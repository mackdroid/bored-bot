#!/usr/bin/env python
global status_react,cl,client,slash
from discord import Webhook, RequestsWebhookAdapter
import discord,atexit,schedule,threading,time
from discord.ext import commands
from discord_slash import SlashCommand
from settings import *
from functions import *
from utilcmds import *

cl = []
client = commands.Bot(command_prefix="/", intents=discord.Intents.all())
slash = SlashCommand(client, sync_commands=True)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

## Daily Schedules
# Daily Reset
def daily_reset():
    cl.clear()
    print("Daily Reset Successful")
    return
schedule.every().day.at("14:00").do(daily_reset)
# Post Daily links
def daily_links():
    webhook = Webhook.from_url(webhooklink, adapter=RequestsWebhookAdapter())
    webhook.send(embeds=[retclasslinks("Time for class","Heres the Links ↓",cl)])     
    print("Sent daily links")
    return
schedule.every().day.at("12:00").do(daily_links)
# daemon thinge
def schedulerd():
    while True:
     schedule.run_pending()
     time.sleep(60) # wait one minute
thread = threading.Thread(target=schedulerd)
thread.daemon = True                            # Daemonize thread
thread.start()                                  # Start the execution
def exit():
    print("\nExiting...")
    return
atexit.register(exit)
client.run(disc_token)
