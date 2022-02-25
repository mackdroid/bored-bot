if __name__ == "__main__":
    print("This is a cog, execute main.py!")
    exit()

# supress sklearn's annoying warnings
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

import nextcord,json # nextcord for discord, json for loading settings
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
from profanity_check import predict_prob # for profanity filter


# import settings from settings.json
vardb = json.load(open("settings.json"))

# setup
def setup(client):
    client.add_cog(utils(client))

class utils(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True) # load unload cogs for debugging purposes
    async def sudo(self,ctx,arg1=None,arg2=None):
        if ctx.message.author.id != vardb["owner_id"]:
            await ctx.send("Access Denied")
            return
        if arg1 == "reload_cog":
            try:
                cog = "cogs."+arg2
                self.client.reload_extension(cog) 
                await ctx.send("Reloaded "+arg2+"!")
            except Exception as e:
                await ctx.send("Error: "+str(e))
        elif arg1 == "unload_cog":
            try:
                cog = "cogs."+arg2
                self.client.unload_extension(cog)
                await ctx.send("Unloaded "+arg2+"!")
            except Exception as e:
                await ctx.send("Error: "+str(e))
        elif arg1 == "load_cog":
            try:
                cog = "cogs."+arg2
                self.client.load_extension(cog)
                await ctx.send("Loaded "+arg2+"!")
            except Exception as e:
                await ctx.send("Error: "+str(e))
        else:
            await ctx.send("Usage: sudo <command> <arg>, where command is one of: reload_cog, unload_cog, load_cog")

    @commands.command(pass_context=True) # purge command for deleting messages
    @commands.has_permissions(administrator=True)
    async def purge(self, ctx, limit:int):
        try:
            await ctx.channel.purge(limit=limit)
            await ctx.send('Cleared by {}'.format(ctx.author.mention),delete_after=3)
        except:
            await ctx.send('Unknown Error, perhaps check permissions?')

    # @nextcord.slash_command(
    #     name="purge",
    #     description="Purge chat content",
    #     default_permission=False
    # )
    # async def slash_purge(self,interaction:Interaction,limit:int):
    #     await interaction.channel.purge(limit=limit)
    #     await interaction.response.send_message('Cleared by {}'.format(interaction.user.mention),delete_after=3)

    @nextcord.slash_command( # change bot status
        name="status",
        description="Set bot status!")
    async def status(self,interaction:Interaction,
        type:str=SlashOption(
        name="type",
        description="Choose status type, i.e Listening, Watching... etc",
        choices={"watching":"Watching","listening":"Listening","playing":"Playing","streaming":"Streaming"},
        required=True),
        status:str=SlashOption(
        name="status",
        description="Set the bot Status",
        required=True)
    ):  
        embed = nextcord.Embed(description=f"{type} {status}",title="Setting Status to") # create embed
        if type == "Listening":
            try:
                await self.client.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.listening, name=f"{status}"))
                await interaction.response.send_message(embed=embed)
            except:
                await interaction.response.send_message("An error occured")
        elif type == "Watching":
            try:
                await self.client.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name=f"{status}"))
                await interaction.response.send_message(embed=embed)
            except:
                await interaction.response.send_message("An error occured")
        elif type == "Playing":
            try:
                await self.client.change_presence(activity=nextcord.Activity(activity=nextcord.Game(name=f"{status}")))
                await interaction.response.send_message(embed=embed)
            except:
                await interaction.response.send_message("An error occured")
        elif type == "Streaming": 
            try:
                await self.client.change_presence(activity=nextcord.Streaming(name=f"{status}",url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")) # you know where the link leads(hopefully)
                await interaction.response.send_message(embed=embed)
            except:
                await interaction.response.send_message("An error occured")
        else:
            return
        
    @nextcord.slash_command(name="ping", # Ping command
    description="Ping pong and view latency",
    )
    async def ping(self,interaction: Interaction):
        embed = nextcord.Embed(title="Pong! 🏓")
        await interaction.response.send_message(embed=embed) # reply with embed
        ping = round(self.client.latency*1000)
        embed.set_footer(text=f"{ping} ms")
        await interaction.edit_original_message(embed=embed) # edit embed with latency

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user: # if message is from bot ignore
            return
        whitelisted_ids = vardb["profCheck"].keys() # get whitelisted ids
        if str(message.guild.id) in whitelisted_ids and "damn" not in message.content: # check if guild is whitelisted
            msg_predict_prob = predict_prob([str(message.content)])[0]*100
            # await message.channel.send("this message has a probability of " + str(msg_predict_prob)+ "% , containing profanity")
            if int(msg_predict_prob) > 82 : # if message contains profanity
                await message.delete()
                channel = self.client.get_channel(vardb["profCheck"][str(message.guild.id)]) # get log channel
                if channel is not None:
                    await channel.send(f"Message containing: ```{message.content}```Deleted in {message.channel.name} sent by {message.author.mention},\nPrediction percentage: {msg_predict_prob}")
                return




