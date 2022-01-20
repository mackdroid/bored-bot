#!/usr/bin/env python
import nextcord
from nextcord.ext import commands
from settings import vardb

from cogs.funcmds import funcmds
from cogs.music import music
from cogs.utils import utils
from cogs.teams import teams

client = commands.Bot(command_prefix=vardb["prefix"], intents=nextcord.Intents.all())

print("Loading Cogs")
client.add_cog(funcmds(client))
client.add_cog(music(client))
client.add_cog(utils(client))
client.add_cog(teams(client))
print("Cogs sucessfully loaded")

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


client.run(vardb["disc_token"])