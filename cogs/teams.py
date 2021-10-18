from discord.ext import commands
from settings import vardb
global cl
import schedule
from discord import Webhook, RequestsWebhookAdapter
from functions import retclasslinks
from discord_slash import SlashContext,cog_ext

class teams(commands.Cog):
    def __init__(self, client,cl):
        self.client = client
        cl = [] 
        # Daily Reset
        def daily_reset():
            cl.clear()
            print("Daily Reset Successful")
            return
        schedule.every().day.at("14:00").do(daily_reset)
        # Post Daily links
        def daily_links():
            webhook = Webhook.from_url(vardb["webhooklink"], adapter=RequestsWebhookAdapter())
            webhook.send(embeds=[retclasslinks("Time for class","Heres the Links ↓",cl)])     
            print("Sent daily links")
            return
        schedule.every().day.at("12:00").do(daily_links)
    @cog_ext.cog_slash( # Command to retrive the class meeting links
        name="classlinks",
        description="Prints class meeting links!",
        guild_ids=[vardb["guildid"]]
        )
    async def links(self,ctx: SlashContext):
        from functions import retclasslinks
        await ctx.send(embeds=[retclasslinks("Class Meetings","Links Go here ↓",self.cl)])

    @commands.Cog.listener()
    async def on_message(self,message):
        if(vardb["scanchannelid"] == str(message.channel.id)):
            if("https://teams.microsoft.com/" in message.content.lower()):
                self.cl.append(message.content)
                await message.add_reaction('✅')