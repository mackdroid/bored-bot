import discord
from discord.opus import DecoderStruct
from discord_slash.utils.manage_commands import create_choice,create_option
from discord_slash import cog_ext
from profanity_check import predict_prob

global vardb,guildID,permissions
from settings import *
guildID = vardb["guildid"]
from discord.ext import commands

class utils(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def purge(self, ctx, limit:int):
        await ctx.channel.purge(limit=limit)
        await ctx.send('Cleared by {}'.format(ctx.author.mention),delete_after=3)

    @cog_ext.cog_slash(
        name="purge",
        description="Purge chat content",
        options=[
            create_option(
                name="messages",
                description="Type the number of messages to deleted",
                required=True,
                option_type=4
            )
        ]
    )
    async def slash_purge(self,ctx,limit:int):
        ctx.invoke(self.client.get_command('purge'), limit=limit)

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

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return
        if int(message.guild.id) in vardb["profcheck_whitelist_ids"]:
            msg_predict_prob=predict_prob([str(message.content)])[0]*100
            # await message.channel.send("this message has a probability of " + str(msg_predict_prob)+ "% , containing profanity")
            if int(msg_predict_prob) > 82 :
                await message.delete()
                channel = self.client.get_channel(vardb["log_ch"])
                await channel.send(f"Message containing: ```{message.content}```Deleted in {message.channel.name} sent by {message.author.mention},\nPrediction percentage: {msg_predict_prob}")
                return




