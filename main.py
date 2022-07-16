#!/usr/bin/env python
import json
from os import listdir

import nextcord
from nextcord.ext import commands

settingsdb = json.load(open("settings.json"))
client = commands.Bot(command_prefix=commands.when_mentioned_or(settingsdb["prefix"]), intents=nextcord.Intents.all())


def main():
    print("Loading cogs...")
    cog_dir = listdir('cogs')
    for cog in cog_dir:
        if cog.endswith('.py'):
            cog = cog[:-3]
            print("Found " + cog + ", Loading..")
            # try:
            #     mod = "cogs."+cog
            #     client.load_extension(mod)
            #     print("Loaded "+cog)
            # except Exception as e:
            #     print("Error loading "+cog+": "+str(e))
            mod = "cogs." + cog
            client.load_extension(mod)
            print("Loaded " + cog)
        else:
            print("Found file " + cog + ", but it does not seem to be a cog.")
    print("Cogs successfully loaded")


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


if __name__ == '__main__':
    main()
    client.run(settingsdb["token"])
