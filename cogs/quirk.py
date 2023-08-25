from nextcord.ext import commands
import re


def setup(client):
    client.add_cog(quirk())


# Class for failry random stuff that are helpful

class quirk(commands.Cog):
    @commands.Cog.listener()
    async def on_message(self, message):
        if "https://www.instagram.com/reel" in message.content:
            webhook = await message.channel.create_webhook(name='hooker')
            await webhook.send(content=re.sub(r'instagram\.com', 'ddinstagram.com', message.content),avatar_url = message.author.avatar.url,username=message.author.display_name)
            await webhook.delete()
            await message.delete()
            return
