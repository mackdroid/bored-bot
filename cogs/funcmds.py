import discord,random
from discord.ext import commands
from discord_slash.utils.manage_commands import create_choice,create_option
from discord_slash import cog_ext

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
