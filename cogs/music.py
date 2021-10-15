from json.decoder import JSONDecoder
from discord.ext import commands
from discord import FFmpegOpusAudio, voice_client
# from settings import vardb
# from discord_slash import SlashContext,cog_ext
import requests,json,re,html,youtube_dl
queue = {}
youtube_dl.utils.bug_reports_message = lambda: '' # supress errors
ytdlOpts = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
}

ytdl = youtube_dl.YoutubeDL(ytdlOpts)

class music(commands.Cog):
    def __init__(self, client):
        self.client = client
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
            url = ytdlData['entries'][0]['formats'][1]['url']
            ret = [url,src,song_artist,song_title]
        elif('https://youtu.be' not in query) or ('https://youtube.com' not in query):
            src = "yts"
            ytdlData = ytdl.extract_info(f"ytsearch:{query}", download=False)
            title = ytdlData['entries'][0]['title']
            url = ytdlData['entries'][0]['formats'][1]['url']
            ret = [url,src,title]
        else:
            src = "yts"
            ytdlData = ytdl.extract_info(query, download=False)
            title = ytdlData
            url = ytdlData['entries'][0]['formats'][1]['url']
            ret = [url,src,title]
        return ret

    @commands.command(aliases=['p'])
    async def play(self,ctx,arg="Never gonna give you up"):
        voice_channel = ctx.author.voice.channel
        voice = ctx.channel.guild.voice_client
        if voice is None:
            voice = await voice_channel.connect()
        elif voice.channel != voice_channel:
            voice.move_to(voice_channel)
        print(arg)
        source = self.arg_handler(arg)
        player = FFmpegOpusAudio(source[0])
        await ctx.send("playing "+ source[2])
        voice.play(player)
    @commands.command(aliases=['j','connect'])
    async def join(self,ctx):
        voice_channel = ctx.author.voice.channel
        voice = ctx.channel.guild.voice_client
        if voice is None:
            voice = await voice_channel.connect()
        elif voice.channel != voice_channel:
            voice.move_to(voice_channel)
        await ctx.send("joined vc")
