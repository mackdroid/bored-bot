#!/usr/bin/env python
from importlib import import_module
import nextcord,json
from os import listdir
from nextcord.ext import commands

vardb = json.load(open("settings.json"))
client = commands.Bot(command_prefix=commands.when_mentioned_or(vardb["prefix"]), intents=nextcord.Intents.all())

def main():
    print("Loading cogs...")
    dir = listdir('cogs')
    for cog in dir:
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

if __name__ == '__main__':
    client.loop.create_task(main())
    client.run(vardb["token"])