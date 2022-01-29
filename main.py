#!/usr/bin/env python
from importlib import import_module
import nextcord,json
from os import listdir
from nextcord.ext import commands

vardb = json.load(open("settings.json"))
client = commands.Bot(command_prefix=vardb["prefix"], intents=nextcord.Intents.all())

print("Loading Cogs")
for cog in listdir('cogs'):
    if cog.endswith('.py'):
        cog = cog[:-3]
        print ("Found "+cog+", Loading..")
        try:
            mod = "cogs."+cog
            client.load_extension(mod)
            print("Loaded "+cog)
        except Exception as e:
            print("Error loading "+cog+": "+str(e))
    else:
        print("Found file "+cog+", but it does not seem to be a cog.")





print("Cogs sucessfully loaded")

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


client.run(vardb["disc_token"])