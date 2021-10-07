#!/usr/bin/env python
global status_react,cl
import discord,atexit,schedule,time,threading
from discord.ext import commands
from discord_slash import SlashCommand
from cogs.utilcmds import utils
from cogs.funcmds import funcmds
from cogs.teams import teams
from settings import vardb
cl = []
client = commands.Bot(command_prefix=vardb["prefix"], intents=discord.Intents.all())
slash = SlashCommand(client, sync_commands=True)
client.add_cog(utils(client,cl=cl))
client.add_cog(teams(client,cl=cl))
client.add_cog(funcmds(client))
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
def exit():
    print("\nExiting...")
    return
atexit.register(exit)
# daemon thinge
def schedulerd():
    while True:
     schedule.run_pending()
     time.sleep(60) # wait one minute
thread = threading.Thread(target=schedulerd)
thread.daemon = True                            # Daemonize thread
print("Started schedule daemon")
client.run(vardb["disc_token"])