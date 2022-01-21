if __name__ == "__main__":
    print("This is a cog, execute main.py!")
    exit()
import queue
from discord.ext import commands
from discord import FFmpegOpusAudio,VoiceClient, guild
from youtube_dl import YoutubeDL
# from settings import vardb
import requests,json,re,html,youtube_dl,discord,asyncio
songqueue = {}
youtube_dl.utils.bug_reports_message = lambda: '' # supress errors
ytdlOpts = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'default_search': 'auto',
}
ffmpegOpts = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'}

class music(commands.Cog):
    def __init__(self, client):
        self.client = client

    def arg_handler(self,query):
        with YoutubeDL(ytdlOpts) as ytdl:
            # if 'https://open.spotify.com/track/' in query:
            #     src = "spot"
            #     response = requests.get(query)
            #     filter = re.search("Spotify.Entity.*};",response.text).group(0)[17:-1]
            #     spotinfo = json.loads(filter)
            #     song_title = html.unescape(spotinfo["album"]["name"])
            #     song_artist = html.unescape(spotinfo['album']['artists'][0]['name'])
            #     searchstr = (song_title + " " + song_artist)
            #     ytdlData = ytdl.extract_info(f"ytsearch:{searchstr}", download=False)
            #     url = ytdlData['entries'][0]['formats'][1]['url']
            #     ret = [url,src,song_title,song_artist]
            # elif('https://youtu.be' not in query) or ('https://youtube.com' not in query):
            if('https://youtu.be' not in query) or ('https://youtube.com' not in query):
                src = "yts"
                ytdlData = ytdl.extract_info(f"ytsearch:{query}", download=False)
                title = ytdlData['entries'][0]['title']
                url = ytdlData['entries'][0]['formats'][1]['url']
                ret = [url,src,title]
            else:
                src = "yts"
                ytdlData = ytdl.extract_info(query, download=False)
                title = ytdlData['entries'][0]['title']
                url = ytdlData['entries'][0]['formats'][1]['url']
                ret = [url,src,title]
            return ret
    @commands.command(aliases=["p","add"])
    async def play(self,ctx: commands.Context,*arg):
        if arg == None:
            arg = "https://youtu.be/dQw4w9WgXcQ"
        authorChannel = ctx.author.voice.channel
        voice = ctx.channel.guild.voice_client
        guild_id=ctx.guild.id
        if authorChannel is None:
            ctx.send("You must be in a vc to use this")
        if voice is None:
            await authorChannel.connect()
            voice = ctx.channel.guild.voice_client
        elif voice.channel != authorChannel:
            voice.move_to(authorChannel)
        if guild_id not in songqueue.keys():
            songqueue[guild_id] = []
        if not voice.is_playing():
            source = self.arg_handler(arg)
            player = FFmpegOpusAudio(source[0], **ffmpegOpts)
            await ctx.send("playing "+ source[2])
            await voice.play(player)
            voice.is_playing()
            while True:
                if len(songqueue[guild_id]) > 0:
                    server_id=ctx.guild.id
                    source = songqueue[server_id][0]
                    player = FFmpegOpusAudio(source[0], **ffmpegOpts)
                    songqueue[server_id].pop(0)
                    await ctx.send("playing "+ source[2])
                    await voice.play(player)
                    voice.is_playing()
                else:
                    await ctx.send("Queue is empty")
                break
        else:
            await ctx.send("Already playing song, Adding to queue")
            server_id=int(ctx.guild.id)
            songqueue[server_id].append(self.arg_handler(arg))
            return

    @commands.command(aliases=["s"])
    async def skip(self,ctx):
        authorChannel = ctx.author.voice.channel
        voice = ctx.channel.guild.voice_client
        guild_id=ctx.guild.id
        if authorChannel is None:
            ctx.send("You must be in a vc to use this")
        if voice is None:
            ctx.send("Bot not in a vc")
        if guild_id not in songqueue.keys():
            songqueue[guild_id] = []
        if len(songqueue[guild_id]) > 0:
            discord.utils.get(self.client.voice_clients, guild=ctx.guild).stop()
            server_id=ctx.guild.id
            source = songqueue[server_id][0]
            player = FFmpegOpusAudio(source[0], **ffmpegOpts)
            songqueue[server_id].pop(0)
            await ctx.send("playing next in queue "+ source[2])
            await voice.play(player)
            voice.is_playing()
        else:
            await ctx.send("Queue is empty")
            return

    @commands.command(aliases=['dump'])
    async def dump_queue(self,ctx):
        await ctx.send(songqueue)

    @commands.command(aliases=['q'])
    async def queue(self,ctx):
        guild_id=ctx.guild.id
        embed = discord.Embed(title="Song Queue")
        for i in songqueue[guild_id]:
            id = songqueue[guild_id].index(i)
            embed.add_field(name=str(id+1)+". "+i[2], value=f"`id {id+1}`",inline=False)
        await ctx.send(embed=embed)

    @commands.command(aliases=['clear'])
    async def stop(self,ctx):
        guild_id=ctx.guild.id
        discord.utils.get(self.client.voice_clients, guild=ctx.guild).stop()
        songqueue[guild_id].clear()
        await ctx.send("Stopped And Cleared queue")

    @commands.command(aliases=['j','connect'])
    async def join(self,ctx):
        authorChannel = ctx.author.voice.channel
        voice = ctx.channel.guild.voice_client
        if authorChannel is None:
            ctx.send("You must be in a vc to use this")
        if voice is None:
            voice = await authorChannel.connect()
        elif voice.channel != authorChannel:
            voice.move_to(authorChannel)
        await ctx.send("Joined your voice channel")

    @commands.command(aliases=['d','disc','leave','fuckoff'])
    async def disconnect(self,ctx):
        authorChannel = ctx.author.voice.channel
        voice = ctx.channel.guild.voice_client
        if authorChannel is None:
            ctx.send("You must be in a vc to use this")
        if voice is None:
            ctx.send("Not in voice channel")
        await voice.disconnect()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if len(self.client.get_guild(id).voice_client.channel.members) < 1:
            asyncio.sleep(180)
            if len(self.client.get_guild(id).voice_client.channel.members) < 1:
                await self.client.get_guild(id).voice_client.disconnect()