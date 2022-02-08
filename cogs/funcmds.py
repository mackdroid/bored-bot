if __name__ == "__main__":
    print("This is a cog, execute main.py!")
    exit()

import nextcord
import random
import json
import requests
from io import BytesIO
from PIL import Image
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
# import settings from settings.json
vardb = json.load(open("settings.json"))

snipedb={}

# setup
def setup(client):
    client.add_cog(funcmds(client))

# setup dpfx for easy access to prefix
dpfx = vardb["prefix"]

# resize image to 1x1 pixels and return colour as hex
def get_dominant_color(image_url):
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    img = img.resize((1, 1))
    data = list(img.getdata())
    rgb = data[0]
    color = nextcord.Color.from_rgb(rgb[0], rgb[1], rgb[2])
    return color

class funcmds(commands.Cog):
    def __init__(self, client):
        self.client = client
    @nextcord.slash_command(name="toss", # Toss a coin
             description="Toss a coin, accepts Heads and Tails as input.",
             )
    async def flip(self,
     interaction: Interaction,
     side=SlashOption(
     name="side",
     description="Choose a side of the coin.",
     required=True,
     choices={"Heads":"Heads","Tails":"Tails"}),
     reason=SlashOption(
      name="reason",
      description="Reason for tossing the coin.",
      required=False)
    ):
        embed = nextcord.Embed(title="Tossing a coin...")
        await interaction.response.send_message(embeds=[embed])
        coin = ["Heads","Tails"]
        if reason is None: # check for reason if none is given set suffix to empty string
          suffix = ""
        else:
          suffix = " for {}".format(reason)
        embed = nextcord.Embed(title=f"The 🪙 flipped to {random.choice(coin)}" + suffix + "!") # choose random choice and embed and reply
        embed.add_field(
            name="Your choice",
            value=f"{side}"
            )
        await interaction.edit_original_message(embeds=[embed])

    def get_meme(self): # Get a meme from reddit
      meme = json.loads(requests.get("https://meme-api.herokuapp.com/gimme").text) # GET meme from api
      embed = nextcord.Embed(title=meme["title"]) # create embed
      embed.set_footer(text="u/" + meme["author"] + " - r/" + meme["subreddit"])
      embed.set_image(url=meme["url"])
      return embed # return meme with embed containing meme

    @nextcord.slash_command(name="meme", # Meme slash comand
    description="Get a random meme from reddit")
    async def meme_slash(self,interaction: Interaction):
      await interaction.response.send_message(embed=self.get_meme()) # send meme with embed

    @commands.command(aliases=['m']) # Meme command
    async def meme(self,ctx):
      await ctx.send(embed=self.get_meme()) # send embed with the meme

    def get_gif(self,category:None,person:None,author:str): # Get a gif from various gif sources
      categories = ["kick","happy","wink","poke","dance","cringe","neko","cat","dog","kill","highfive","happy"]
      prefix = ""
      ishelp = False
      if person == None: # check for variable
        person = random.choice(["himself..?","themselves.."])
        noarg2 = True
      else:
        person = person.mention
      if category == "kick" or category == "kill" or category == "highfive": # check for category
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
      elif category == "waifu":
        suffix = "heres yer waifu"
        apiurl = "https://api.waifu.pics/sfw/" + category
      elif category == "dog":
        suffix = random.choice([f"'s {category}! 🐶","doggo!! 🐶"])
        apiurl = "https://api.thedogapi.com/v1/images/search"
      elif category == "help":
        ishelp = True
      else:
        prefix = "well" + " "
        suffix = "thats a unknown category, heres a cat instead!"
        apiurl = "https://api.thecatapi.com/v1/images/search"
      if ishelp == False: # check if category is help, if yes get gif from the set apiurl
        if (apiurl.find('waifu') != -1):
          url = json.loads(requests.get(apiurl).text)["url"]
        else:
          url = json.loads(requests.get(apiurl).text)[0]["url"]
        color = get_dominant_color(url)
        embed = nextcord.Embed(description=prefix + author + " " + suffix , color=color)
        footer = random.choice([f"use `{dpfx}gif help` for more more categories","UwU","owo"])
        embed.set_footer(text=footer)
        embed.set_image(url=url)
      else: # if help set embed to help menu
        embed=nextcord.Embed(title="Usage", description=f"{dpfx}g/gif [subcategory] [person]")
        embed.add_field(name="Available Subcategories", value="waifu, kick, happy, wink, poke, dance, cringe, neko, cat, dog, kill, highfive, happy", inline=False)
      return embed

    @commands.command(aliases=['g'])
    async def gif(self,ctx,category=None,person : nextcord.Member=None):
      try:
        await ctx.send(embed=self.get_gif(category,person,ctx.message.author.mention))
      except Exception as e:
        embed = nextcord.Embed(title="Something went wrong, try again later.", description=e)
        await ctx.send(embed=embed)

    @nextcord.slash_command(name="gif", # Send a gif from random apis
            description="Send a GIF from different categories")
    async def gif_slash(self, interaction:Interaction,
    category: str = SlashOption(
        name="category",
        choices={"waifu":"waifu","kick":"kick","happy":"happy","wink":"wink","poke":"poke","dance":"dance","cringe":"cringe","neko":"neko","cat":"cat","dog":"dog","kill":"kill","highfive":"highfive","happy":"happy","help":"help"},
        description="Choose a category to get a gif from",
    ),
    person:nextcord.Member = SlashOption(
      name="person",
      required=False, 
      description="Choose a person to send the GIF to.")):
      await interaction.response.send_message(embed=self.get_gif(category,person,interaction.user.mention))

    @commands.command(aliases=['av'])
    async def avatar(self, ctx, *,  avamember:nextcord.Member=None):
      if avamember == None:
        avamember = ctx.message.author
      avaurl = avamember.display_avatar.url
      color = get_dominant_color(avaurl)
      embed = nextcord.Embed(title=avamember.name + "'s avatar", color=color)
      embed.set_image(url=avaurl)
      await ctx.send(embed=embed)
      
    @commands.command(aliases=['sn'])
    async def snipe(self,ctx):
      chanid = ctx.message.channel.id
      if chanid not in snipedb.keys():
        snipedb[chanid] = {}
        embed = nextcord.Embed(title="No messages have been sniped in this channel yet.",description="How unfortunate!")
        await ctx.send(embed=embed)
      else:
        content = snipedb[chanid]['content']
        author = snipedb[chanid]['author']
        embed = nextcord.Embed(title="Sniped message (ゝ‿ മ)",description=content)
        embed.add_field(name="Sent by: ",value=author)
        await ctx.send(embed=embed)
        
    @commands.Cog.listener()
    async def on_message_delete(self,message):
      if message.author.bot == False:
        if message.content.startswith(dpfx):
          return
        else:
          author = message.author.mention
          chanid = message.channel.id
          content = message.content
          dict = {'content':content,'author':author}
          if chanid not in snipedb.keys():
            snipedb[chanid] = {}
          snipedb[chanid] = dict