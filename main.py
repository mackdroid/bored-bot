global status_react, cl
from discord import Webhook, RequestsWebhookAdapter
import discord,atexit,random,schedule,threading,time,asyncio
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice,create_option
from settings import *
from functions import *
cl = []
client = commands.Bot(command_prefix="/", intents=discord.Intents.all())
slash = SlashCommand(client, sync_commands=True)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@slash.slash( # Status
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
async def status(ctx,type,status):
    embed = discord.Embed(description=f"{type} to {status}",title="Setting Status to")
    message = await ctx.send(embed=embed) 
    if type == "Listening":
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"{status}"))
        await message.add_reaction(status_react)
    elif type == "Watching":
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{status}"))
        await message.add_reaction(status_react)
    elif type == "Playing":
        await client.change_presence(activity=discord.Activity(activity=discord.Game(name=f"{status}")))
        await message.add_reaction(status_react)
    elif type == "Streaming":
        await client.change_presence(activity=discord.Streaming(name=f"{status}",url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"))# you know where the link leads
        await message.add_reaction(status_react)
    else:
        await ctx.send("how tf did you get here")

@slash.slash(  # mute
    name="mute",
    description="Banish a person into the shadow realm.",
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
async def mute(ctx,member,time,reason):
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


@slash.slash( # unmute
    name="unmute",
    description="unmute a person manually",
    options=[
        create_option(
            name="member",
            description="Choose a member",
            required=True,
            option_type=6
        )
    ]
)
async def unmute(ctx, member):
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

@slash.slash(name="toss", # Toss a coin 
             description="Toss a coin, accepts Heads and Tails as input.",
             options=[
               create_option(
                 name="side",
                 description="Choose a side of the coin.",
                 option_type=3,
                 required=True,
                 choices=[
                  create_choice(
                    name="Heads",
                    value="heads"
                  ),
                  create_choice(
                    name="Tails",
                    value="tails"
                  )
                ]
               )
             ])
async def flip(ctx,side):
    coin = ['heads','tails']
    embed = discord.Embed(title=f"The 🪙 flipped to {random.choice(coin)}!" )
    embed.add_field(
        name="Your choice",
        value=f"{side}"
        )
    await ctx.send(embeds=[embed])

@slash.slash(name="ping", # Ping command
description="Ping pong and view latency",
guild_ids=guildid
)
async def ping(ctx):
    ping = client.latency*1000
    embed = discord.Embed(title="Pong! 🏓")
    embed.set_footer(text=f"{ping} ms")
    await ctx.send(embeds=[embed]) 

@slash.slash( # Command to retrive the class meeting links
    name="classlinks",
    description="Prints class meeting links!",
    guild_ids=guildid
    )
async def links(ctx: SlashContext):
    await ctx.send(embeds=[retclasslinks("Class Meetings","Links Go here ↓",cl)])

@client.event # Scan for messages containing a certain string and add them to the CL string
async def on_message(message):
    if(scanchannelid == str(message.channel.id)):
        if("https://teams.microsoft.com/" in message.content.lower()):
            cl.append(message.content)
            await message.add_reaction('✅')

## Daily Schedules
# Daily Reset
def daily_reset():
    cl.clear()
    print("Daily Reset Successful")
    return
schedule.every().day.at("13:00").do(daily_reset)
# Post Daily links
def daily_links():
    webhook = Webhook.from_url(webhooklink, adapter=RequestsWebhookAdapter())
    webhook.send(embeds=[retclasslinks("Time for class","Heres the Links ↓",cl)])     
    print("Sent daily links")
    return
schedule.every().day.at("07:59").do(daily_links)

# daemon thinge
def schedulerd():
    while True:
     schedule.run_pending()
     time.sleep(60) # wait one minute
thread = threading.Thread(target=schedulerd)
thread.daemon = True                            # Daemonize thread
thread.start()                                  # Start the execution

def exit():
    print("\nExiting...")
    return
atexit.register(exit)
client.run(disc_token)
