from discord.ext import commands
from discord import FFmpegOpusAudio
# from settings import vardb
import requests,json,re,html,youtube_dl,discord,asyncio
queue = {}
youtube_dl.utils.bug_reports_message = lambda: '' # supress errors
ytdlOpts = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
}
ffmpegOpts = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'}
ytdl = youtube_dl.YoutubeDL(ytdlOpts)

class music(commands.Cog):
    def __init__(self, client):
        self.client = client
        queue = {}
    def arg_handler(self,query):
        if 'https://open.spotify.com/track/' in query:
            src = "spot"
            response = requests.get(query)
            filter = re.search("Spotify.Entity.*};",response.text).group(0)[17:-1]
            spotinfo = json.loads(filter)
            song_title = html.unescape(spotinfo["album"]["name"])
            song_artist = html.unescape(spotinfo['album']['artists'][0]['name'])
            searchstr = (song_title + " " + song_artist)
            ytdlData = ytdl.extract_info(f"ytsearch:{searchstr}", download=False)
            url = ytdlData['url']
            ret = [url,src,song_title,song_artist]
        elif('https://youtu.be' not in query) or ('https://youtube.com' not in query):
            src = "yts"
            ytdlData = ytdl.extract_info(f"ytsearch:{query}", download=False)
            title = ytdlData['title']
            url = ytdlData['url']
            ret = [url,src,title]
        else:
            src = "yts"
            ytdlData = ytdl.extract_info(query, download=False)
            title = ytdlData['title']
            url = ytdlData['url']
            ret = [url,src,title]
        return ret

    @commands.command(aliases=['p'])
    async def play(self,ctx,*arg): 
        if arg == None:
            arg = "Never gonna give you up"
        voice_channel = ctx.author.voice.channel
        voice = ctx.channel.guild.voice_client
        if voice is None:
            voice = await voice_channel.connect()
        elif voice.channel != voice_channel:
            voice.move_to(voice_channel)
            source = self.arg_handler(arg)
            player = FFmpegOpusAudio(source[0], **ffmpegOpts)
            await ctx.send("playing "+ source[2])
            voice.play(player)
            voice.is_playing()

    @commands.command(aliases=['s','stop'])
    async def skip(self,ctx):
        discord.utils.get(self.client.voice_clients, guild=ctx.guild).stop()
        await ctx.send("stopped")

    @commands.command(aliases=['j','connect'])
    async def join(self,ctx):
        voice_channel = ctx.author.voice.channel
        voice = ctx.channel.guild.voice_client
        if voice is None:
            voice = await voice_channel.connect()
        elif voice.channel != voice_channel:
            voice.move_to(voice_channel)
        await ctx.send("joined vc")

    @commands.command(aliases=['d','disc','leave','fuckoff'])
    async def disconnect(self,ctx):
        voice = ctx.channel.guild.voice_client
        if voice is None:
            ctx.send("not in vc")
        await voice.disconnect()

    # @commands.Cog.listener()
    # async def on_voice_state_update(self, member, before, after):
    #     if len(self.bot.get_guild(id).voice_client.channel.members) < 1:
    #         asyncio.sleep(180)
    #         if len(self.bot.get_guild(id).voice_client.channel.members) < 1:
    #             await self.bot.get_guild(id).voice_client.disconnect()