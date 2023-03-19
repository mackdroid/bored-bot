if __name__ == "__main__":
    print("This is a cog, execute main.py!")
    exit()

from ast import arg
import json
import random
from io import BytesIO

import nextcord
import nextcord as nc
import requests
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


gif_lst = {'kick': ['https://i.waifu.pics/FxDWcmZ.gif',
  'https://i.waifu.pics/wZtL4zy.gif',
  'https://i.waifu.pics/BZ38S3s.gif',
  'https://i.waifu.pics/~9t_55m.gif',
  'https://i.waifu.pics/wZtL4zy.gif',
  'https://i.waifu.pics/Qjuht_q.gif'],
 'happy': ['https://i.waifu.pics/Ck_nyHx.gif',
  'https://i.waifu.pics/E_tAOv2.gif',
  'https://i.waifu.pics/Ck_nyHx.gif',
  'https://i.waifu.pics/M4kkraV.gif',
  'https://i.waifu.pics/LcFeEJz.gif',
  'https://i.waifu.pics/7Kz7bE1.gif'],
 'wink': ['https://i.waifu.pics/87KteDJ.gif',
  'https://i.waifu.pics/87KteDJ.gif',
  'https://i.waifu.pics/QmF2rf1.gif',
  'https://i.waifu.pics/y1E0H4g.gif',
  'https://i.waifu.pics/W4_OW_P.gif',
  'https://i.waifu.pics/t2IcbQK.gif'],
 'poke': ['https://i.waifu.pics/s446j9L.gif',
  'https://i.waifu.pics/JlDu4xg.gif',
  'https://i.waifu.pics/A4SyFip.gif',
  'https://i.waifu.pics/s446j9L.gif',
  'https://i.waifu.pics/jWRdbHV.jpg',
  'https://i.waifu.pics/SkfA6gM.gif'],
 'dance': ['https://i.waifu.pics/l0ysv60.gif',
  'https://i.waifu.pics/aUJPpXN.gif',
  'https://i.waifu.pics/jJCputQ.gif',
  'https://i.waifu.pics/oI~t28j.gif',
  'https://i.waifu.pics/iVDuV9y.gif',
  'https://i.waifu.pics/u0uOEKf.gif'],
 'cringe': ['https://i.waifu.pics/mjqxv04.gif',
  'https://i.waifu.pics/osLWoRP.gif',
  'https://i.waifu.pics/gkB-aJ2.jpg',
  'https://i.waifu.pics/jdZCreG.gif',
  'https://i.waifu.pics/aV0bggk.gif',
  'https://i.waifu.pics/zZXPRJY.gif'],
 'kill': ['https://i.waifu.pics/hGFuwrQ.gif',
  'https://i.waifu.pics/aHcQUmi.gif',
  'https://i.waifu.pics/lgsRSai.gif',
  'https://i.waifu.pics/ETWB-ef.gif',
  'https://i.waifu.pics/9b1NpBN.gif',
  'https://i.waifu.pics/8uhQSdY.gif'],
 'highfive': ['https://i.waifu.pics/NUusyu4.gif',
  'https://i.waifu.pics/UPcalVj.gif',
  'https://i.waifu.pics/JvYGKhE.gif',
  'https://i.waifu.pics/6oy99g3.gif',
  'https://i.waifu.pics/gJaFVbX.gif',
  'https://i.waifu.pics/Q_pkTt4.gif'],
 'pat': ['https://i.waifu.pics/rOU~HpB.gif',
  'https://i.waifu.pics/kSE4Ypd.gif',
  'https://i.waifu.pics/0x-pKQY.gif',
  'https://i.waifu.pics/MqgjYTF.gif',
  'https://i.waifu.pics/UQ~PSLN.gif',
  'https://i.waifu.pics/I~znmj2.gif'],
 'kiss': ['https://i.waifu.pics/-DGDccm.gif',
  'https://i.waifu.pics/I0fKKlq.gif',
  'https://i.waifu.pics/aSe6WAS.gif',
  'https://i.waifu.pics/6ApTQ4Z.gif',
  'https://i.waifu.pics/h3IJio-.gif',
  'https://i.waifu.pics/h3IJio-.gif']}



class funcmds(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def choose(ctx,*argv):
        await ctx.send("I Choose",random.choice(argv),"!") 

    @nc.slash_command(name="toss",  # Toss a coin
                      description="Toss a coin, accepts Heads and Tails as input.",
                      )
    async def flip(self,
                   interaction: Interaction,
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
        await interaction.edit_original_message(embeds=[embed])

    # def get_meme(self):  # Get a meme from reddit
    #     meme = json.loads(requests.get("https://meme-api.herokuapp.com/gimme").text)  # GET meme from api
    #     embed = nc.Embed(title=meme["title"])  # create embed
    #     embed.set_footer(text="u/" + meme["author"] + " - r/" + meme["subreddit"])
    #     embed.set_image(url=meme["url"])
    #     return embed  # return meme with embed containing meme

    # @nc.slash_command(name="meme",  # Meme slash comand
    #                   description="Get a random meme from reddit")
    # async def meme_slash(self, interaction: Interaction):
    #     await interaction.response.send_message(embed=self.get_meme())  # send meme with embed

    # @commands.command(aliases=['m'])  # Meme command
    # async def meme(self, ctx):
    #     await ctx.send(embed=self.get_meme())  # send embed with the meme

    def get_gif(self, category, person, author, selfp:False):  # Get a gif from various gif sources
        # categories = ["kick","happy","wink","poke","dance","cringe","neko","cat","dog","kill","highfive","happy","pat"]
        prefix = ""
        ishelp = False
        if person == None:  # check for variable
            person = random.choice(["himself..?", "themselves.."])
            noarg2 = True
            
        if category == "highfive":
            suffix = category + f"s {person}!"
        elif category == "happy":
            suffix = "is happy :D!"
        elif category == "wink" or category == "poke" or category == "cringe":
            replies = ["'s! whew", f"'s at {person}!"]
            if noarg2 == True and category == "wink" or category == "cringe":
                reply = random.choice(replies)
            else:
                reply = f"'s at {person}!"
            suffix = category + reply
        elif category == "dance":
            suffix = f"dance's with {person}!"
        elif category == "neko" or category == "cat":
            suffix = f"'s {category}! 🐈"
            apiurl = "https://api.thecatapi.com/v1/images/search"
        elif category == "waifu":
            suffix = "heres yer waifu"
        elif category == "dog":
            suffix = random.choice([f"'s {category}! 🐶", "doggo!! 🐶"])
            apiurl = "https://api.thedogapi.com/v1/images/search"
        elif category == "kiss":
            suffix = random.choice([f"kisses {person}!", f"gives a peck to {person}!"])
        elif category == "pat":
            suffix = random.choice([f"pats {person}!", f"gently pats {person}!"])
        elif category == "kick" or category == "kill":  # check for category
            if selfp == True:
                suffix = f"aww, dont be so hard on yourself\n*pats* {author}"
                author = ""
                category = "pat"
            else:
                suffix = category + f"s {person}!\nMust've been a baka"
        elif category == "help":
            ishelp = True
        else:
            category = "cat"
            prefix = "Well" + " "
            suffix = "thats a unknown category, heres a cat instead!"
            apiurl = "https://api.thecatapi.com/v1/images/search"
            
        if ishelp != True:  # check if category is help, if yes get gif from the set apiurl
            if category in ["dog","cat"]:
                url = json.loads(requests.get(apiurl).text)[0]["url"]
            else:
                url = random.choice(gif_lst[category])
            # color = get_dominant_color(url) # causes a lot of lag disabled for now
            embed = nc.Embed(description=prefix + author + " " + suffix, color=0x5ce8ed)
            footer = random.choice([f"use `{dpfx}gif help` for more more categories", "uwu", "OwO"])
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
            selfp = False
            if person == ctx.author:
                person = None
                selfp = True
            if person is not None:
                person = person.mention
            await ctx.send(embed=self.get_gif(category, person, ctx.message.author.mention,selfp))
        except Exception as e:
            embed = nc.Embed(title="Something went wrong, try again later.", description=e)
            await ctx.send(embed=embed)

    @nc.slash_command(name="gif",  # Send a gif from random apis
                      description="Send a GIF from different categories")
    async def gif_slash(self, interaction: Interaction,
                        category: str = SlashOption(
                            name="category",
                            choices={"waifu": "waifu", "kick": "kick", "wink": "wink", "poke": "poke", "dance": "dance",
                                     "cringe": "cringe", "cat": "cat", "dog": "dog", "kill": "kill",
                                     "highfive": "highfive", "happy": "happy", "help": "help"},
                            description="Choose a category to get a gif from",
                        ),
                        person: nc.Member = SlashOption(
                            name="person",
                            required=False,
                            description="Choose a person to send the GIF to.")):
        if interaction.author == person:
            person = None
            selfp = True
        if person is not None:
            person = person.mention
        else:
            person = None
        await interaction.response.send_message(embed=self.get_gif(category, person, interaction.user.mention,selfp))

    @commands.command(aliases=['av'])
    async def avatar(self, ctx, *, avamember: nc.Member = None):
        if avamember == None:
            avamember = ctx.message.author
        avaurl = avamember.display_avatar.url
        color = 0xffffff
        #color = get_dominant_color(avaurl)
        embed = nc.Embed(title=avamember.name + "'s avatar", color=color)
        embed.set_image(url=avaurl)
        await ctx.send(embed=embed)
        
    @commands.command(aliases=['sav'])
    async def server_avatar(self, ctx):
        guild = ctx.guild
        color = 0xffffff
        #color = get_dominant_color(guild.icon.url)
        embed = nc.Embed(title=guild.name + "'s Server Icon", color=color)
        embed.set_image(url=guild.icon.url)
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

        @nextcord.ui.button(label='⬅️', style=nextcord.ButtonStyle.green)
        async def prev(self, button, ictx):
            if await self.check_author(ictx) == False:
                return
            if self.page == 0:
                return
            else:
                self.page -= 1
            await ictx.response.edit_message(embed=self.format_page(self.page), view=self)

        @nextcord.ui.button(label='➡️', style=nextcord.ButtonStyle.green)
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
        for i in dpfx:
            if message.content.startswith(i):
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
        n = 5
        if len(snipedb[chanid]) > n:
            snipedb[chanid].pop(n)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        for i in dpfx:
            if before.content.startswith(i):
                return
        if before.author.bot == True:
            return
        if before.author.id == self.client.user.id:
            return
        if str(before.guild.id) in list(settingsdb['profCheck'].keys()):
            return
        chanid = before.channel.id
        dat = {'before': before, 'after': after}
        if chanid not in editdb.keys():
            editdb[chanid] = []
        editdb[chanid].insert(0, dat)
        n = 5
        if len(editdb[chanid]) > n:
            editdb[chanid].pop(n)
