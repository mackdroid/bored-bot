if __name__ == "__main__":
    print("This is a cog, execute main.py!")
    exit()

# imports
import queue
import nextcord
from nextcord.ext import commands
from nextcord import FFmpegOpusAudio, guild
from youtube_dl import YoutubeDL
import requests,json,re,html,youtube_dl,discord,asyncio

# initialize queue
songqueue = {}
colors = {
    "error" : 0xf54257,
    "success" : 0x6cf257,
    "neutral" : 0x43ccc3
}

youtube_dl.utils.bug_reports_message = lambda: '' # supress errors

# set up youtube_dl
ytdlOpts = {
    'format': 'bestaudio/best',
    'noplaylist': True,
    'default_search': 'auto',
}
# set up ffmpeg options 
ffmpegOpts = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -reconnect_on_network_error 1',
    'options': '-vn'}

# setup
def setup(client):
    client.add_cog(music(client))

class player:
    
    def args_to_url(self,args): # convert parse search query to ytdl urls
        if type(args) is tuple:
            args = " ".join(args)
        with YoutubeDL(ytdlOpts) as ytdl:
            if args.find("https://open.spotify.com")==0:
                src = "spot"
                response = requests.get(args)
                filter = re.search("\"entities\":.*\"podcasts\"",response.text).group(0)[11:-11] # scrape the spotify link for the track id
                response = json.loads(filter)
                song_title = html.unescape(response["items"][list(response["items"].keys())[0]]["name"])
                song_artist = html.unescape(response["items"][list(response["items"].keys())[0]]["artists"]["items"][0]["profile"]["name"])
                searchstr = (song_title + " " + song_artist)
                ytdlData = ytdl.extract_info(f"ytsearch:{searchstr}", download=False) # search for the song from youtube
                url = ytdlData['entries'][0]['formats'][1]['url']
                thumb = response["items"][list(response["items"].keys())[0]]["album"]["coverArt"]["sources"][0]["url"] # get the thumbnail
                return url,src,thumb,song_title+" by "+song_artist # return the url, source, thumbnail, and song title
            elif args.find('https://youtu.be')==0 or args.find('https://youtube.com')==0:
                src = "yts"
                ytdlData = ytdl.extract_info(args, download=False) # get song data from url using youtube_dl
                title = ytdlData['entries'][0]['title']
                url = ytdlData['entries'][0]['formats'][1]['url']
                thumb = ytdlData['entries'][0]['thumbnails'][0]['url']
                return url,src,thumb,title # return the url, source, thumbnail, and song title
            else:
                src = "yts"
                ytdlData = ytdl.extract_info(f"ytsearch:{args}", download=False) # search for the song from youtube using youtube-dl 
                title = ytdlData['entries'][0]['title']
                url = ytdlData['entries'][0]['formats'][1]['url']
                thumb = ytdlData['entries'][0]['thumbnail']
                return url,src,thumb,title # return the url, source, thumbnail, and song title

    def ensure_voice(ctx): # check if the bot is in the same voice channel as the user
        def aw(arg):
            asyncio.get_event_loop().run(arg)
        guild_id=ctx.guild.id
        voice = ctx.channel.guild.voice_client
        authorChannel = ctx.author.voice.channel if ctx.author.voice else None
        if authorChannel is None:
            embed = nextcord.Embed(title="You must be in a voice channel to use this.",color=colors["error"])
            aw(ctx.send(embed=embed))
        else:    
            if guild_id not in songqueue.keys():
                songqueue[guild_id] = []
            if voice is None:
                aw(ctx.author.voice.channel.connect())
                embed = nextcord.Embed(title="Connected to your voice channel.", color=colors["success"])
                aw(ctx.send(embed=embed))
            elif ctx.author.voice.channel is not voice.channel:
                aw(voice.move_to(ctx.author.voice.channel))
                embed = nextcord.Embed(title="Inconsistency in bot's channel, Moved to your voice channel.", color=colors["neutral"])
                aw(ctx.send(embed=embed))
            aw(ctx.guild.change_voice_state(channel=ctx.author.voice.channel, self_mute=False, self_deaf=True))

    async def play(ctx,arg): # play a song
        if arg == ():
                embed = nextcord.Embed(title="Please enter a search query.",description="Youtube and spotify links are accepted, if otherwise query terms will be considered as youtube search terms",color=0xf54257)
                await ctx.send(embed=embed)
                return
        player.ensure_voice(ctx)
        guild_id = ctx.guild.id
        if guild_id not in songqueue.keys():
            songqueue[guild_id] = []
        voice = ctx.channel.guild.voice_client
        if voice.is_playing():
            
            song = player.args_to_url(arg)
            url,src,thumb,title = song
            songqueue[guild_id].append(song)
            color = colors["spot"] if src == "spot" else colors["yts"] 
            embed = nextcord.Embed(title="Playing "+ title, color=colors["success"], colour=color)
            embed.set_thumbnail(url=thumb)
            vclient = player.player(ctx,url)
            await ctx.send(embed=embed)
            await player.queue_handler(ctx)
            if vclient is not None:
                embed = nextcord.Embed(title="A Player error occured:",description=Exception,color=colors["error"])
                await ctx.send(embed=embed)

    def player(ctx,url):
        voice = ctx.channel.guild.voice_client
        player = FFmpegOpusAudio(url, **ffmpegOpts)
        try:
            voice.play(player)
        except:
            return Exception
        voice.is_playing()
        return 

    async def queue(ctx):
        guild_id=ctx.guild.id
        if guild_id not in songqueue.keys():
                songqueue[guild_id] = []
        voice = ctx.channel.guild.voice_client
        description = ""
        embed = discord.Embed(title="Song Queue", description=description, color=0x613583)
        if voice is not None and voice.is_playing():
            description = "Now playing: "+songqueue[guild_id][0][3]
            embed.set_description(description)
            embed.set_thumbnail(url=songqueue[guild_id][0][2])
        if len(songqueue[guild_id]) > 1:
            for i in songqueue[guild_id]:
                if i == songqueue[guild_id][0]:
                    continue
                id = songqueue[guild_id].index(i)
                embed.add_field(name=str(id+1)+". "+i[3], value=f"`id {id+1}`",inline=False)
        else:
            embed.add_field(name="No songs in queue", value="songs are added automatically to queue when there is already a song playing",inline=False)
        await ctx.send(embed=embed)

    async def queue_handler(self,ctx,arg):
        voice = ctx.channel.guild.voice_client
        guild_id=ctx.guild.id
        if voice is None:
            embed = nextcord.Embed(title="Bot not in a voice channel to continue",color=colors["error"])
            await ctx.send(embed=embed)
            return
        if guild_id not in songqueue.keys():
            songqueue[guild_id] = []
        while True:
            if len(songqueue[guild_id]) > 1:
                if arg == "skip":
                    voice.stop()
                for i in range(3):
                    server_id=ctx.guild.id
                    url,src,thumb,title = songqueue[server_id][0]
                    player = self.player(ctx,url)
                    if player is None:
                        color = colors["spot"] if src == "spot" else colors["yts"] 
                        embed = nextcord.Embed(title="Playing "+ title, color=colors["success"], colour=color)
                        embed.set_thumbnail(url=thumb)
                        await ctx.send(embed=embed)
                        songqueue[server_id].pop(0)       
                        break
                    else:
                        embed = nextcord.Embed(title="A Player error occured:",description=Exception,color=colors["error"])
                        await ctx.send(embed=embed)
                        if i == 2:
                            embed = nextcord.Embed(title="Failed to play song, removing from queue",color=colors["error"])
                            await ctx.send(embed=embed)
                            songqueue[server_id].pop(0)
                            break
            else:
                if arg != "next":
                    embed = nextcord.Embed(title="Queue is empty", description="Add some using the play/add command", color=colors["neutral"])
                    await ctx.send(embed=embed)
                break

    async def stop(ctx):
        voice = ctx.channel.guild.voice_client
        if voice is not None:
            await voice.stop()
            songqueue[guild.id].clear()
            embed = nextcord.Embed(title="Stopped playing music, and cleared song queue", color=0x6cf257)
        else:
            embed = nextcord.Embed(title="Bot not in a voice channel", color=0xf54257)
        await ctx.send(embed=embed)


class music(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="play",aliases=["p","add","a"]) # play command
    async def play(self,ctx,*args):
        await player.play(ctx,args)

    @commands.command(name="queue",aliases=["q","list","l"]) # list the queue
    async def queue(self,ctx):
        await player.queue(ctx)

    @commands.command(name="skip",aliases=["s","next"]) # skip the current song
    async def skip(self,ctx):
        await player.queue_handler(ctx,"skip")

    @commands.command(name="stop",aliases=["st","end","fuckoff"]) # stop the bot from playing music
    async def stop(self,ctx):
        await player.stop(ctx)

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