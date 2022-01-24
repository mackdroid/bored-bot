if __name__ == "__main__":
    print("This is a cog, execute main.py!")
    exit()
# imports
from ast import While
import queue
import nextcord
from nextcord.ext import commands
from nextcord import FFmpegOpusAudio
from youtube_dl import YoutubeDL
import requests,json,re,html,youtube_dl,discord,asyncio
# initialize queue
songqueue = {}

youtube_dl.utils.bug_reports_message = lambda: '' # supress errors
# set up youtube_dl
ytdlOpts = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'default_search': 'auto',
}
# set up ffmpeg options 
ffmpegOpts = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 1',
    'options': '-vn'}

class music(commands.Cog):
    def __init__(self, client):
        self.client = client

    def arg_handler(self,query):
        res = " ".join(query)
        with YoutubeDL(ytdlOpts) as ytdl:
            if res.find("https://open.spotify.com")==0:
                src = "spot"
                response = requests.get(res)
                filter = re.search("\"entities\":.*\"podcasts\"",response.text).group(0)[11:-11]
                response = json.loads(filter)
                song_title = html.unescape(response["items"][list(response["items"].keys())[0]]["name"])
                song_artist = html.unescape(response["items"][list(response["items"].keys())[0]]["artists"]["items"][0]["profile"]["name"])
                searchstr = (song_title + " " + song_artist)
                ytdlData = ytdl.extract_info(f"ytsearch:{searchstr}", download=False)
                url = ytdlData['entries'][0]['formats'][1]['url']
                thumb = response["items"][list(response["items"].keys())[0]]["album"]["coverArt"]["sources"][0]["url"]
                ret = [url,src,thumb,song_title+" by "+song_artist]
            elif res.find('https://youtu.be')==0 or res.find('https://youtube.com')==0:
                src = "yts"
                ytdlData = ytdl.extract_info(res, download=False)
                title = ytdlData['entries'][0]['title']
                url = ytdlData['entries'][0]['formats'][1]['url']
                thumb = ytdlData['entries'][0]['thumbnails'][0]['url']
                ret = [url,src,thumb,title]
            else:
                src = "yts"
                ytdlData = ytdl.extract_info(f"ytsearch:{res}", download=False)
                title = ytdlData['entries'][0]['title']
                url = ytdlData['entries'][0]['formats'][1]['url']
                thumb = ytdlData['entries'][0]['thumbnail']
                ret = [url,src,thumb,title]
            return ret

    def queue_embed(self,ctx):
        guild_id=ctx.guild.id
        if guild_id not in songqueue.keys():
                songqueue[guild_id] = []
        embed = discord.Embed(title="Song Queue", description="", color=0x613583)
        if len(songqueue[guild_id]) > 0:
            for i in songqueue[guild_id]:
                id = songqueue[guild_id].index(i)
                embed.add_field(name=str(id+1)+". "+i[3], value=f"`id {id+1}`",inline=False)
        else:
            embed.add_field(name="No songs in queue", value="songs are added automatically to queue when there is already a song playing",inline=False)
        return embed

    async def ensure_voice(self,ctx):
        guild_id=ctx.guild.id
        voice = ctx.channel.guild.voice_client
        authorChannel = ctx.author.voice.channel if ctx.author.voice else None
        if authorChannel is None:
            embed = nextcord.Embed(title="You must be in a voice channel to use this.",color=0xf54257)
            await ctx.send(embed=embed)
        else:    
            if guild_id not in songqueue.keys():
                songqueue[guild_id] = []
            if voice is None:
                await ctx.author.voice.channel.connect()
                embed = nextcord.Embed(title="Connected to your voice channel.", color=0x6cf257)
                await ctx.send(embed=embed)
            elif ctx.author.voice.channel is not voice.channel:
                await voice.move_to(ctx.author.voice.channel)
                embed = nextcord.Embed(title="Inconsistency in bot's channel, Moved to your voice channel.", color=0x6cf257)
                await ctx.send(embed=embed)
            await ctx.guild.change_voice_state(channel=ctx.author.voice.channel, self_mute=False, self_deaf=True)

    async def player(self,ctx,query):
        voice = ctx.channel.guild.voice_client
        player = FFmpegOpusAudio(query[0], **ffmpegOpts)
        try:
            voice.play(player)
        except:
            embed = nextcord.Embed(title="A Player error occured:",description=Exception,color=0xf54257)
            await ctx.send(embed=embed)
        voice.is_playing()
        embed = nextcord.Embed(title="Playing "+ query[3], color=0x6cf257)
        await ctx.send(embed=embed)

    async def queue_handler(self,ctx,skip):
        voice = ctx.channel.guild.voice_client
        guild_id=ctx.guild.id
        if voice is None:
            embed = nextcord.Embed(title="Bot not in a voice channel to continue",color=0xf54257)
            await ctx.send(embed=embed)
            return
        if guild_id not in songqueue.keys():
            songqueue[guild_id] = []
        while True:
            if len(songqueue[guild_id]) > 0:
                if skip == True:
                    voice.stop()
                server_id=ctx.guild.id
                source = songqueue[server_id][0]
                await self.player(ctx,source)
                songqueue[server_id].pop(0)
            else:
                embed = nextcord.Embed(title="Queue is empty", description="Add some using the play/add command", color=0x43ccc3)
                await ctx.send(embed=embed)
                break

    @commands.command(aliases=["p","add"])
    async def play(self,ctx: commands.Context,*arg):
        if arg == ():
            embed = nextcord.Embed(title="Please enter a search query.",description="Youtube and spotify links are accepted, if otherwise query terms will be considered as youtube search terms",color=0xf54257)
            await ctx.send(embed=embed)
            return
        await self.ensure_voice(ctx)
        voice = ctx.channel.guild.voice_client
        if not voice.is_playing():
            query = self.arg_handler(arg)
            await self.player(ctx,query)
            await self.queue_handler(ctx,False)
        else:
            server_id=int(ctx.guild.id)
            query = self.arg_handler(arg)
            songqueue[server_id].append(query)
            embed = nextcord.Embed(title="Already playing song", description=f"**Added {query[3]} to queue**", color=0x43ccc3)
            await ctx.send(embed=embed)

    @commands.command(aliases=["s"])
    async def skip(self,ctx):
        await self.queue_handler(ctx,True)

    @commands.command(aliases=['dump'])
    async def dump_queue(self,ctx):
        await ctx.send(songqueue)

    @commands.command(aliases=['q'])
    async def queue(self,ctx):
        embed = self.queue_embed(ctx)
        await ctx.send(embed=embed)

    @commands.command(aliases=['clear'])
    async def stop(self,ctx):
        guild=ctx.guild
        voice = discord.utils.get(self.client.voice_clients, guild=guild.id)
        if voice is not None:
            await voice.stop()
            songqueue[guild.id].clear()
            embed = nextcord.Embed(title="Stopped playing music, and cleared song queue", color=0x6cf257)
        else:
            embed = nextcord.Embed(title="Bot not in a voice channel", color=0xf54257)
        await ctx.send(embed=embed)

    @commands.command(aliases=['j','connect'])
    async def join(self,ctx):
        await self.ensure_voice(ctx)

    @commands.command(aliases=['d','disc','leave','fuckoff'])
    async def disconnect(self,ctx):
        authorChannel = ctx.author.voice.channel
        voice = ctx.channel.guild.voice_client
        if authorChannel is None:
            embed = nextcord.Embed(title="You must be in a voice channel to use this.",color=0xf54257)
            await ctx.send(embed=embed)
        if voice is None:
            embed = nextcord.Embed(title="Bot not in voice channel",color=0xf54257)
            await ctx.send(embed=embed)
        await voice.disconnect()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after): # checks if there are more than one person in the voice channel or else leaves
        if member.id == self.client.user.id:
            return
        voice = discord.utils.get(self.client.voice_clients, guild=member.guild)
        if voice is None:
            return
        voice_channel = voice.channel
        member_count = len(voice_channel.members)
        if member_count == 1:
            await asyncio.sleep(30)
            if member_count == 1:
                await voice.disconnect()