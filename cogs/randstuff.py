from nextcord.ext import commands


def setup(client):
    client.add_cog(rand())


# Class for random stuff

class rand(commands.Cog):
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.content == "is gaeeeeeeeeeee":
            await message.delete()
            return
