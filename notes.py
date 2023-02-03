import nextcord as nc
from nextcord.ext import commands

class notes(commands.Cog):
    @commands.command()
    async def createnote(ctx,name,val**):
        