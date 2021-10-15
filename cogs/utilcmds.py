import discord,asyncio
from discord_slash.utils.manage_commands import create_choice,create_option
from discord_slash import SlashContext,cog_ext

global vardb,guildID,permissions
from settings import *
guildID = vardb["guildid"]
from discord.ext import commands

class utils(commands.Cog):
    def __init__(self, client,cl):
        self.client = client
        self.cl = cl
        
    @cog_ext.cog_slash( # Status
        name="status",
        description="Set bot status!",
        options=[
            create_option(
                name="type",
                description="Choose status type, i.e Listening, Watching... etc",
                option_type=3,
                required=True,
                choices=[
                    create_choice(
                        name="Listening",
                        value="Listening"
                    ),
                   create_choice(
                        name="Watching",
                       value="Watching"
                    ),
                    create_choice(
                        name="Playing",
                        value="Playing"
                    ),
                    create_choice(
                        name="Streaming",
                        value="Streaming"
                    )              
                ]
            ),
            create_option(
                name="status",
                description="Set the bot Status",
                option_type=3,
                required=True
            )
        ]
    )
    async def status(self,ctx,type,status):
        embed = discord.Embed(description=f"{type} {status}",title="Setting Status to")
        message = await ctx.send(embed=embed) 
        if type == "Listening":
            await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"{status}"))
            await message.add_reaction(vardb["status_react"])
        elif type == "Watching":
            await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{status}"))
            await message.add_reaction(vardb["status_react"])
        elif type == "Playing":
            await self.client.change_presence(activity=discord.Activity(activity=discord.Game(name=f"{status}")))
            await message.add_reaction(vardb["status_react"])
        elif type == "Streaming": 
            await self.client.change_presence(activity=discord.Streaming(name=f"{status}",url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"))# you know where the link leads
            await message.add_reaction(vardb["status_react"])
        else:
            await ctx.send("how tf did you get here")

    @cog_ext.cog_slash(  # mute
        name="mute",
        description="Banish a person into the shadow realm.",
        permissions=permissions,
        guild_ids=[guildID],
        options=[
            create_option(
                name="member",
                description="Choose a member",
                option_type=6,
                required=True
            ),
            create_option(
                name="time",
                description="Choose a time",
                option_type=3,
                required=True,
                choices=[
                    create_choice(
                        name="1m",
                        value="1m"
                    ),
                    create_choice(
                        name="5m",
                        value="5m"
                    ),
                     create_choice(
                        name="10m",
                        value="10m"
                    ),
                    create_choice(
                        name="30m",
                        value="30m"
                    ),
                    create_choice(
                        name="1h",
                        value="1h"
                    ),
                    create_choice(
                        name="2h",
                        value="2h"
                    ),
                    create_choice(
                        name="6h",
                        value="6h"
                    ),                
                    create_choice(
                        name="12h",
                        value="12h"
                    ),
                    create_choice(
                        name="24h",
                        value="24h"
                    ),
                ]
            ),
            create_option(
                name="reason",
                description="Choose a reason",
                option_type=3,
                required=True
            )
        ]
    )
    async def mute(self,ctx,member,time,reason):
        # variables to declare 
        server = ctx.guild
        author = ctx.author
        mutedRole = discord.utils.get(server.roles, name="muted") # looks for muted role
        # Triggers a discord error 10062
        # if muted role doesn't exist
        # if not mutedRole:
        #     mutedRole = await server.create_role(name="muted") # creates muted role
        # for channel in server.channels:
        #     await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=True) # sets muted role permissions
        # mute
        await member.add_roles(mutedRole, reason=reason) # adds muted role
        # embed
        mutedEmbed = discord.Embed(title=f"{member.name}#{member.discriminator} was muted by {author.name}#{author.discriminator}") # creating an embed for the mute command
        mutedEmbed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar_url) # adding an author to the embed
        mutedEmbed.add_field(name="reason", value=f"{reason}") # adding a field to the embed
        mutedEmbed.add_field(name="duration", value=f"{time}") # adding a field to the embed
        # sends content
        await member.send(embed=mutedEmbed) # DMs the member the embed we just made
        await ctx.send(embed=mutedEmbed) # sends the embed we just made 
        # convert min/hours into seconds
        if time.endswith("m") and str.isdigit(time[:-1:]):
            timeS = int(time[:-1:]) * 60
        elif time.endswith("h") and str.isdigit(time[:-1:]):
            timeS = int(time[:-1:]) * 3600
        # mute time 
        await asyncio.sleep(timeS) # timer
        # unmute
        await member.remove_roles(mutedRole) # removes muted role
        # embed
        unmuteEmbed = discord.Embed(title=f"{member.name}#{member.discriminator}'s mute has ended") # creating an embed for the automatic unmute stage
        unmuteEmbed.set_author(name=f"{member.name}#{member.discriminator}", icon_url=member.avatar_url) # adding an author to the embed
        # sends content
        await member.send(embed=unmuteEmbed) # DMs the member the embed we just made 

    @cog_ext.cog_slash( # unmute
        name="unmute",
        description="unmute a person manually",
        permissions=permissions,
        guild_ids=[guildID],
        options=[
            create_option(
                name="member",
                description="Choose a member",
                required=True,
                option_type=6
            )
        ]
    )
    async def unmute(self, ctx, member):
        server = ctx.guild
        author = ctx.author
        mutedRole = discord.utils.get(server.roles, name = "muted")
        # unmute
        await member.remove_roles(mutedRole) # removes muted role
        # embed 
        manualunmuteEmbed = discord.Embed(title=f"{member.name}#{member.discriminator} was unmuted by {author.name}#{author.discriminator}") # creating an embed for the manual unmute command 
        manualunmuteEmbed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar_url) # adding an author to the embed 
        # sends content
        await member.send(embed=manualunmuteEmbed) # DMs the user the embed we just made 
        await ctx.send(embed=manualunmuteEmbed)

    


