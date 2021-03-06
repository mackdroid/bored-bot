if __name__ == "__main__":
    print("This is a cog, execute main.py!")
    exit()

# imports
import json
import nextcord
from nextcord import Interaction
from nextcord.ext import commands

# load settings from settings.json
vardb = json.load(open("settings.json"))


# setup
def setup(client):
    if "teams" in vardb.keys():
        client.add_cog(teams(client))
    else:
        print("No teams key found in settings.json, disabling cog.")


# Setup cl var to be used to store the class links
global cl
cl = []


# returns the classlinks in a embed
def retclasslinks(title, desc, cl):
    classlinkembed = nextcord.Embed(title=title, description=desc)
    if len(cl) == 0:
        classlinkembed.add_field(name="Ive got no links, no classes i guess", value="¯\_(ツ)_/¯")
    else:
        for i in cl:
            mytitle = i[:i.find('http')]
            print(len(mytitle))
            if (len(mytitle) == 0):
                mytitle = "Class Link(no title found)"
            classlinkembed.add_field(name='> ' + mytitle, value=i[i.find('http'):] + '\n\n', inline=False)
    return classlinkembed


class teams(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(  # Command to retrive the class meeting links
        name="classlinks",
        description="Prints class meeting links!",
        guild_ids=vardb["teams"]["TeamsWhitelistIds"]
    )
    async def links(self, interaction: Interaction):
        from functions import retclasslinks
        await interaction.response.send_message(embeds=[retclasslinks("Time for class", "Heres the Links ↓", cl)])

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id in vardb["teams"]["ScanChIds"]:
            if ("https://teams.microsoft.com/" in message.content.lower()):
                self.cl.append(message.content)
                await message.add_reaction('✅')

    # @commands.Cog.listener()
    # async def on_ready(self):
    #     while True:
    #         now = datetime.now()
    #         seconds_to_event = round((timedelta(hours=24) - (now - now.replace(hour=7, minute=50, second=0, microsecond=0))).total_seconds() % (24 * 3600))
    #         await asyncio.sleep(seconds_to_event) # Calculate the time until the next 7:50am (when my online classes start) in seconds
    #         for channel in vardb["teams"]["DailyPostlinkChIds"]:
    #             await self.client.get_channel(channel).send(embeds=[retclasslinks("Time for class","Heres the Links ↓",cl)])
    #         await asyncio.sleep(18600)
    #         cl.clear() # clear the list containing class links
    #         # repeat
