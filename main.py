#!/usr/bin/env python
import discord
from discord.ext import commands
from cogs.music import music
from cogs.utils import utils
from cogs.funcmds import funcmds
# from cogs.teams import teams
from settings import vardb
client = commands.Bot(command_prefix=vardb["prefix"], intents=discord.Intents.all())


print("Loading Cogs")
client.add_cog(funcmds(client))
client.add_cog(music(client))
client.add_cog(utils(client))
# client.add_cog(teams())
print("Cogs sucessfully loaded")

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

client.run(vardb["disc_token"])