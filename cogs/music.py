from discord.ext import commands
from discord import FFmpegOpusAudio,VoiceClient
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

    def queue_handler(guildid,type,song): # Handles queue, song must be a list with [0] as name and [1] as artist
        if type == "add": #Add
            songqueue[guildid][0].append(song)
        elif type == "del" and type(song) is int or None: # delete from queue
            if song == None:
                song = 1
            del songqueue[guildid][0][song-1]
        elif type == "nxt": # return next in queue or return nothing if queue empty, also remove song from queue after returning song
            if songqueue[guildid] == None or len(songqueue[guildid][0]) == 0:
                return
            else:
                song = songqueue[guildid][0][0]
                del songqueue[guildid][0][0]
                return song
        else:
            return None     

    def arg_handler(self,query):
        with YoutubeDL(ytdlOpts) as ytdl:
            if 'https://open.spotify.com/track/' in query:
                src = "spot"
                response = requests.get(query)
                filter = re.search("Spotify.Entity.*};",response.text).group(0)[17:-1]
                spotinfo = json.loads(filter)
                song_title = html.unescape(spotinfo["album"]["name"])
                song_artist = html.unescape(spotinfo['album']['artists'][0]['name'])
                searchstr = (song_title + " " + song_artist)
                ytdlData = ytdl.extract_info(f"ytsearch:{searchstr}", download=False)
                url = ytdlData['entries'][0]['formats'][1]['url']
                ret = [url,src,song_title,song_artist]
            elif('https://youtu.be' not in query) or ('https://youtube.com' not in query):
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
        if authorChannel is None:
            ctx.send("You must be in a vc to use this")
        if voice is None:
            await authorChannel.connect()
            voice = ctx.channel.guild.voice_client
        elif voice.channel != authorChannel:
            voice.move_to(authorChannel)
        if not voice.is_playing():
            source = self.arg_handler(arg)
            player = FFmpegOpusAudio(source[0], **ffmpegOpts)
            await ctx.send("playing "+ source[2])
            voice.play(player)
            voice.is_playing()
        else:
            await ctx.send("Already playing song, Adding to queue")

            return

    @commands.command(aliases=['s','clear'])
    async def stop(self,ctx):
        discord.utils.get(self.client.voice_clients, guild=ctx.guild).stop()
        await ctx.send("Stopped")

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
        if len(self.bot.get_guild(id).voice_client.channel.members) < 1:
            asyncio.sleep(180)
            if len(self.bot.get_guild(id).voice_client.channel.members) < 1:
                await self.bot.get_guild(id).voice_client.disconnect()