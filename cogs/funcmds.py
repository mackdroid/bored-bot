if __name__ == "__main__":
    print("This is a cog, execute main.py!")
    exit()

import json
import random
from io import BytesIO

import nextcord
import nextcord as nc
import requests
from PIL import Image
from nextcord import Interaction, SlashOption
from nextcord.ext import commands

# import settings from settings.json
settingsdb = json.load(open("settings.json"))
snipedb = {}
editdb = {}


# setup
def setup(client):
    client.add_cog(funcmds(client))


# setup dpfx for easy access to prefix
dpfx = settingsdb["prefix"]


# resize image to 1x1 pixels and return colour as hex
def get_dominant_color(image_url):
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    # img = img.resize((1, 1), Image.NEAREST) # todo fix this awful shit
    data = list(img.getdata())
    rgb = random.choice(data)
    color = nc.Color.from_rgb(rgb[0], rgb[1], rgb[2])
    return color


def get_dominant_color(image_url):
    image = Image.open(requests.get(image_url, stream=True).raw)
    image = image.resize((16, 16))
    r, g, b = image.split()
    r = sum(i * j for i, j in zip(r.getdata(), [1, 4, 6, 4, 1]))
    g = sum(i * j for i, j in zip(g.getdata(), [1, 4, 6, 4, 1]))
    b = sum(i * j for i, j in zip(b.getdata(), [1, 4, 6, 4, 1]))
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

class funcmds(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nc.slash_command(name="toss",  # Toss a coin
                      description="Toss a coin, accepts Heads and Tails as input.",
                      )
    async def flip(self,
                   interaction: Interaction,
                   side=SlashOption(
                       name="side",
                       description="Choose a side of the coin.",
                       required=True,
                       choices={"Heads": "Heads", "Tails": "Tails"}),
                   reason=SlashOption(
                       name="reason",
                       description="Reason for tossing the coin.",
                       required=False)
                   ):
        embed = nc.Embed(title="Tossing a coin...")
        await interaction.response.send_message(embeds=[embed])
        coin = ["Heads", "Tails"]
        if reason is None:  # check for reason if none is given set suffix to empty string
            suffix = ""
        else:
            suffix = " for {}".format(reason)
        embed = nc.Embed(
            title=f"The 🪙 flipped to {random.choice(coin)}" + suffix + "!")  # choose random choice and embed and reply
        embed.add_field(
            name="Your choice",
            value=f"{side}"
        )
        await interaction.edit_original_message(embeds=[embed])

    def get_meme(self):  # Get a meme from reddit
        meme = json.loads(requests.get("https://meme-api.herokuapp.com/gimme").text)  # GET meme from api
        embed = nc.Embed(title=meme["title"])  # create embed
        embed.set_footer(text="u/" + meme["author"] + " - r/" + meme["subreddit"])
        embed.set_image(url=meme["url"])
        return embed  # return meme with embed containing meme

    @nc.slash_command(name="meme",  # Meme slash comand
                      description="Get a random meme from reddit")
    async def meme_slash(self, interaction: Interaction):
        await interaction.response.send_message(embed=self.get_meme())  # send meme with embed

    @commands.command(aliases=['m'])  # Meme command
    async def meme(self, ctx):
        await ctx.send(embed=self.get_meme())  # send embed with the meme

    def get_gif(self, category, person, author):  # Get a gif from various gif sources
        # categories = ["kick","happy","wink","poke","dance","cringe","neko","cat","dog","kill","highfive","happy"]
        prefix = ""
        ishelp = False
        if person == None:  # check for variable
            person = random.choice(["himself..?", "themselves.."])
            noarg2 = True
        if category == "kick" or category == "kill" or category == "highfive":  # check for category
            suffix = category + f"s {person}!"
            apiurl = "https://api.waifu.pics/sfw/" + category
        elif category == "happy":
            suffix = "is happy :D!"
            apiurl = "https://api.waifu.pics/sfw/" + category
        elif category == "wink" or category == "poke" or category == "cringe":
            replies = ["'s! whew", f"'s at {person}!"]
            if noarg2 == True and category == "wink" or category == "cringe":
                reply = random.choice(replies)
            else:
                reply = f"'s at {person}!"
            suffix = category + reply
            apiurl = "https://api.waifu.pics/sfw/" + category
        elif category == "dance":
            suffix = f"dance's with {person}!"
            apiurl = "https://api.waifu.pics/sfw/" + category
        elif category == "neko" or category == "cat":
            suffix = f"'s {category}! 🐈"
            apiurl = "https://api.thecatapi.com/v1/images/search"
        elif category == "waifu":
            suffix = "heres yer waifu"
            apiurl = "https://api.waifu.pics/sfw/" + category
        elif category == "dog":
            suffix = random.choice([f"'s {category}! 🐶", "doggo!! 🐶"])
            apiurl = "https://api.thedogapi.com/v1/images/search"
        elif category == "kiss":
            suffix = random.choice([f"kisses {person}!", f"gives a peck to {person}!"])
            apiurl = "https://api.waifu.pics/sfw/" + category
        elif category == "pat":
            suffix = random.choice([f"pats {person}!", f"gently pats {person}!"])
        elif category == "help":
            ishelp = True
        else:
            prefix = "well" + " "
            suffix = "thats a unknown category, heres a cat instead!"
            apiurl = "https://api.thecatapi.com/v1/images/search"
        if ishelp == False:  # check if category is help, if yes get gif from the set apiurl
            if (apiurl.find('waifu') != -1):
                url = json.loads(requests.get(apiurl).text)["url"]
            else:
                url = json.loads(requests.get(apiurl).text)[0]["url"]
            # color = get_dominant_color(url) # causes a lot of lag disabled for now
            embed = nc.Embed(description=prefix + author + " " + suffix, color=0x5ce8ed)
            footer = random.choice([f"use `{dpfx}gif help` for more more categories", "uwu", "owo"])
            embed.set_footer(text=footer)
            embed.set_image(url=url)
        else:  # if help set embed to help menu
            embed = nc.Embed(title="Usage", description=f"{dpfx}g/gif [subcategory] [person]")
            embed.add_field(name="Available Subcategories",
                            value="waifu, kick, happy, wink, poke, dance, cringe, neko, cat, dog, kill, highfive, happy, pat, kiss",
                            inline=False)
        return embed

    @commands.command(aliases=['g'])
    async def gif(self, ctx, category=None, person: nc.Member = None):
        try:
            try:
                person = person.mention
            except:
                person = None
            await ctx.send(embed=self.get_gif(category, person, ctx.message.author.mention))
        except Exception as e:
            embed = nc.Embed(title="Something went wrong, try again later.", description=e)
            await ctx.send(embed=embed)

    @nc.slash_command(name="gif",  # Send a gif from random apis
                      description="Send a GIF from different categories")
    async def gif_slash(self, interaction: Interaction,
                        category: str = SlashOption(
                            name="category",
                            choices={"waifu": "waifu", "kick": "kick", "wink": "wink", "poke": "poke", "dance": "dance",
                                     "cringe": "cringe", "neko": "neko", "cat": "cat", "dog": "dog", "kill": "kill",
                                     "highfive": "highfive", "happy": "happy", "help": "help"},
                            description="Choose a category to get a gif from",
                        ),
                        person: nc.Member = SlashOption(
                            name="person",
                            required=False,
                            description="Choose a person to send the GIF to.")):
        try:
            person = person.mention
        except:
            person = None
        await interaction.response.send_message(embed=self.get_gif(category, person, interaction.user.mention))

    @commands.command(aliases=['av'])
    async def avatar(self, ctx, *, avamember: nc.Member = None):
        if avamember == None:
            avamember = ctx.message.author
        avaurl = avamember.display_avatar.url
        color = get_dominant_color(avaurl)
        embed = nc.Embed(title=avamember.name + "'s avatar", color=color)
        embed.set_image(url=avaurl)
        await ctx.send(embed=embed)

    class SnipePagination(nextcord.ui.View):
        def __init__(self, author, type, data):
            super().__init__()
            self.data = data
            self.type = type
            self.page = 0
            self.author = author

        async def check_author(self, ictx):
            if ictx.user != self.author:
                await ictx.response.send_message("Not your command pal, make your own using the command `snipe` :v",
                                                 ephemeral=True)
                return False
            else:
                return True

        def format_page(self, page):
            embed = nc.Embed(title="Sniped message (ゝ‿ മ)", color=0x5ce8ed)
            if self.type == "snipe":
                message = self.data[self.page]
                embed.add_field(name="Author", value=message.author.mention, inline=False)
                embed.add_field(name="Message",
                                value=message.content if message.content != "" else "No message content", inline=False)
                # if message.attachments != []: # Disabled for now
                #   attach = ""
                #   n = 1
                #   for i in message.attachments:
                #     attach += f"[Attachment{n}]({i.url})\n"
                #     n+=1
                #   embed.add_field(name="Attachments", value=attach, inline=False)
            elif self.type == "snipeedit":
                before = self.data[self.page]["before"]
                after = self.data[self.page]["after"]
                embed.add_field(name="Author", value=before.author.mention, inline=False)
                embed.add_field(name="Before", value="  **Message**\n  " + (
                    before.content if before.content != "" else "No message content"), inline=False)
                embed.add_field(name="After", value="  **Message**\n  " + (
                    after.content.replace("\n", "\n  ") if after.content != "" else "No message content"), inline=False)
            embed.set_footer(text="Page: " + str(self.page + 1) + "/" + str(len(self.data)))
            return embed

        @nextcord.ui.button(label='🡰', style=nextcord.ButtonStyle.green)
        async def prev(self, button, ictx):
            if await self.check_author(ictx) == False:
                return
            if self.page == 0:
                return
            else:
                self.page -= 1
            await ictx.response.edit_message(embed=self.format_page(self.page), view=self)

        @nextcord.ui.button(label='🡲', style=nextcord.ButtonStyle.green)
        async def next(self, button, ictx):
            if await self.check_author(ictx) == False:
                return
            if self.page >= (len(self.data) - 1):
                return
            else:
                self.page += 1
            await ictx.response.edit_message(embed=self.format_page(self.page), view=self)

        # @nextcord.ui.button(label='🛑', style=nextcord.ButtonStyle.green)
        # async def stop(self, button, ictx):
        #   if await self.check_author(ictx) == False:
        #     return
        #   self.stop()

    @commands.command(aliases=['sn'])
    async def snipe(self, ctx):
        chanid = ctx.message.channel.id
        servid = ctx.message.guild.id
        if str(servid) in list(settingsdb['profCheck'].keys()):
            embed = nc.Embed(title="Snipe disabled due to conflicts with profanity check")
            return await ctx.send(embed=embed)
        try:
            data = snipedb[chanid]
            member = data[0]
            content = member.content
            author = member.author.mention
            embed = nc.Embed(title="Sniped message (ゝ‿ മ)", description=content, color=0x5ce8ed)
            embed.add_field(name="Sent by: ", value=author)
            embed.set_footer(text="Page: 1/" + str(len(data)))
            author = ctx.message.author
            view = self.SnipePagination(author, "snipe", data)
            await ctx.send(embed=embed, view=view)
        except KeyError:
            embed = nc.Embed(title="No messages have been sniped in this channel yet.", description="How unfortunate!")
            await ctx.send(embed=embed)
            return

    @commands.command(aliases=['es'])
    async def editsnipe(self, ctx):
        chanid = ctx.message.channel.id
        servid = ctx.message.guild.id
        if str(servid) in list(settingsdb['profCheck'].keys()):
            embed = nc.Embed(title="Snipe disabled due to conflicts with profanity check")
            await ctx.send(embed=embed)
            return
        try:
            author = ctx.message.author
            data = editdb[chanid]
            before = data[0]["before"]
            after = data[0]["after"]
            embed = nc.Embed(title="Sniped message (ゝ‿ മ)", color=0x5ce8ed)
            embed.add_field(name="Author", value=before.author.mention, inline=False)
            embed.add_field(name="Before", value="  **Message**\n  " + (
                before.content if before.content != "" else "No message content"), inline=False)
            embed.add_field(name="After", value="  **Message**\n  " + (
                after.content.replace("\n", "\n  ") if after.content != "" else "No message content"), inline=False)
            embed.set_footer(text="Page: 1/" + str(len(data)))
            view = self.SnipePagination(author, "snipeedit", data)
            await ctx.send(embed=embed, view=view)
        except KeyError:
            embed = nc.Embed(title="No messages have been edited in this channel yet.", description="How unfortunate!")
            await ctx.send(embed=embed)
            return

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.content.startswith(dpfx):
            return
        if message.author.bot == True:
            return
        if message.author.id == self.client.user.id:
            return
        if len(message.content) < 2:
            return
        if str(message.guild.id) in list(settingsdb['profCheck'].keys()):
            return
        chanid = message.channel.id
        if chanid not in snipedb.keys():
            snipedb[chanid] = []
        snipedb[chanid].insert(0, message)
        if len(snipedb[chanid]) > 5:
            snipedb[chanid].pop(5)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.content.startswith(dpfx):
            return
        if before.author.bot == True:
            return
        if before.author.id == self.client.user.id:
            return
        if str(before.guild.id) in list(settingsdb['profCheck'].keys()):
            return
        chanid = before.channel.id
        dict = {'before': before, 'after': after}
        if chanid not in editdb.keys():
            editdb[chanid] = []
        print("editdb: " + str(dict))
        editdb[chanid].insert(0, dict)
        if len(editdb[chanid]) > 5:
            editdb[chanid].pop(5)
