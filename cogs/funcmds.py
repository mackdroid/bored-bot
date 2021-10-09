import discord,random,json,requests,praw
from discord.ext import commands
from discord_slash.utils.manage_commands import create_choice,create_option
from discord_slash import cog_ext
from settings import vardb
dpfx = vardb["prefix"]

class funcmds(commands.Cog):
    def __init__(self, client):
        self.client = client
    @cog_ext.cog_slash(name="toss", # Toss a coin 
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
    async def flip(self, ctx,side):
        coin = ['heads','tails']
        embed = discord.Embed(title=f"The 🪙 flipped to {random.choice(coin)}!" ) # choose random choice and embed and reply
        embed.add_field(
            name="Your choice",
            value=f"{side}"
            )
        await ctx.send(embeds=[embed])

    @cog_ext.cog_slash(name="ping", # Ping command
    description="Ping pong and view latency",
    )
    async def ping(self,ctx):
        ping = self.client.latency*1000
        embed = discord.Embed(title="Pong! 🏓")
        embed.set_footer(text=f"{ping} ms")
        await ctx.send(embeds=[embed]) 

    @commands.command(aliases=['t'])
    async def truth(self,ctx):
      await ctx.send("")
    @commands.command(aliases=['m'])
    async def meme(self,ctx):
      memesubreddits = ["meme","memes","dankmemes"]
      reddit = praw.Reddit()
      meme = reddit.subreddit(random.choice(memesubreddits)).random()
      embed=discord.Embed(title=meme.title)
      embed.set_footer(text=meme.author)
      embed.set_image(url=meme.url)
      await ctx.send(embed=embed)

    @commands.command(aliases=['g'])
    async def gif(self,ctx,category=None,person : discord.Member=None):
      categories = ["kick","happy","wink","poke","dance","cringe","neko","cat","dog","kill","highfive","happy"]
      prefix = ""
      ishelp = False
      if person == None:
        person = random.choice(["himself..?","themselves.."])
        noarg2 = True
      else:
        person = person.mention
      if category == "kick" or category == "kill" or category == "highfive":
        suffix = category +f"s {person}!"
        apiurl = "https://api.waifu.pics/sfw/" + category
      elif category == "happy":
        suffix = "is happy :D!"
        apiurl = "https://api.waifu.pics/sfw/" + category
      elif category == "wink" or category == "poke" or category == "cringe":
        replies = ["'s! whew",f"'s at {person}!"]
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
      elif category == "dog":
        suffix = random.choice([f"'s {category}! 🐶","doggo!! 🐶"])
        apiurl = "https://api.thedogapi.com/v1/images/search"
      elif category == "help":
        ishelp = True
      else:
        prefix = "well" + " "
        suffix = "thats a unknown category, heres a cat instead!"
        apiurl = "https://api.thecatapi.com/v1/images/search"
      if ishelp == False:
        if (apiurl.find('waifu') != -1):
          url = json.loads(requests.get(apiurl).text)["url"]
        else:
          url = json.loads(requests.get(apiurl).text)[0]["url"]
        embed = discord.Embed(description=prefix + ctx.message.author.mention + " " + suffix) 
        footer = random.choice([f"use `{dpfx}gif help` for more more categories","UwU","owo"])
        embed.set_footer(text=footer)
        embed.set_image(url=url)
      else:
        embed=discord.Embed(title="Usage", description=f"{dpfx}g/gif [subcategory] [person]")
        embed.add_field(name="Available Subcategories", value="kick, happy, wink, poke, dance, cringe, neko, cat, dog, kill, highfive, happy", inline=False)
      await ctx.send(embed=embed)