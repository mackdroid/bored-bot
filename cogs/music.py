if __name__ == "__main__":
    print("This is a cog, execute main.py!")
    exit()

import asyncio
import json

import nextcord as nc
import requests
import youtube_dl
from nextcord import FFmpegOpusAudio
from nextcord.ext import commands
from youtube_dl import YoutubeDL

# initialize queue
songqueue = {}
colors = {
    "error": 0xf54257,
    "success": 0x6cf257,
    "neutral": 0x43ccc3,
    "spotify": 0x1db954,
    "youtube": 0xc4302b,
    "fallback": 0xc7979,
    "apple": 0xfc3c44,
    "other": 0xeba434
}

youtube_dl.utils.bug_reports_message = lambda: ''  # supress errors

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
    voices = client.voice_clients
    songqueue.clear()
    if voices is not None:
        for voice in voices:
            client.loop.create_task(voice.disconnect())
    client.add_cog(music(client))


class QUEUE():
    def now_playing(self, ctx):
        guild_id = ctx.guild.id
        if ctx.guild.id not in songqueue.keys():
            songqueue[guild_id] = []
        voice = ctx.channel.guild.voice_client
        if voice is None:
            return None
        if voice.is_playing():
            return songqueue[guild_id][0]

    def get_current_song(self, ctx):
        guild_id = ctx.guild.id
        if ctx.guild.id not in songqueue.keys():
            songqueue[guild_id] = []
        voice = ctx.channel.guild.voice_client
        if voice is None:
            return None
        return songqueue[guild_id][0]

    def next(self, ctx):
        guild_id = ctx.guild.id
        if len(songqueue[guild_id]) > 1:
            songqueue[guild_id].pop(0)
            return songqueue[guild_id][0]
        else:
            songqueue[guild_id] = []
            return None

    def clear(self, ctx):
        guild_id = ctx.guild.id
        songqueue[guild_id] = []
        return None

    def args_to_url(self, ctx, args):  # convert parse search query to ytdl urls
        if type(args) is tuple:
            args = " ".join(args)
        with YoutubeDL(ytdlOpts) as ytdl:
            if args.find("https://") != -1 or args.find("http://") != -1:
                if args.find("https://www.youtube.com") != -1 or args.find("https://youtu.be") != -1:
                    src = "youtube"
                    ytdl_data = ytdl.extract_info(args, download=False)
                    title = ytdl_data['title']
                    url = ytdl_data['formats'][1]['url']
                    thumb = ytdl_data['thumbnail']
                    return url, src, thumb, title
                else:
                    args = args.replace(" ", "")
                    if args.find("spotify") != -1:
                        src = "spotify"
                    elif args.find("apple") != -1:
                        src = "apple"
                    else:
                        src = "other"
                    apiurl = "https://api.song.link/v1-alpha.1/links?url=" + args  # using odesli for getting youtube link
                    try:
                        response = json.loads(requests.get(apiurl).text)
                        song_title = response["entitiesByUniqueId"][response["entityUniqueId"]]["title"]
                        song_artist = response["entitiesByUniqueId"][response["entityUniqueId"]]["artistName"]
                        thumb = response["entitiesByUniqueId"][response["entityUniqueId"]]["thumbnailUrl"]
                        yturl = response["linksByPlatform"]["youtube"]["url"]
                        ytdl_data = ytdl.extract_info(yturl, download=False)  # search for the song from youtube
                        url = ytdl_data['formats'][1]['url']
                        title = song_title + " by " + song_artist
                        return url, src, thumb, title  # return the url, source, thumbnail, and song title
                    except:
                        return ()
            else:
                src = "youtube"
                ytdl_data = ytdl.extract_info(f"ytsearch:{args}", download=False)  # search for the song from youtube using youtube-dl
                title = ytdl_data['entries'][0]['title']
                url = ytdl_data['entries'][0]['formats'][1]['url']
                thumb = ytdl_data['entries'][0]['thumbnail']
                return url, src, thumb, title  # return the url, source, thumbnail, and song title

    def add(self, ctx, arg):
        if ctx.guild.id not in songqueue.keys():
            songqueue[ctx.guild.id] = []
        lst = self.args_to_url(ctx, arg)
        if lst != ():
            url, src, thumb, title = lst 
            songqueue[ctx.guild.id].append([url, src, thumb, title, ctx])
            return url, src, thumb, title, ctx
        else:
            raise Exception("Song wasn't found.")
        

    def remove(self, ctx, id):
        if ctx.guild.id not in songqueue.keys():
            songqueue[ctx.guild.id] = []
        songqueue[ctx.guild.id].pop(id)
        return None

    def clear(self, ctx):
        songqueue[ctx.guild.id] = []
        return None

class PLAYER():
    def __init__(self, client) -> None:
        self.client = client

    def player(self, ctx, url):
        voice = ctx.channel.guild.voice_client
        guildid = ctx.guild.id
        player = FFmpegOpusAudio(url, **ffmpegOpts)
        after = lambda err: self.after(guildid, err)
        try:
            voice.play(player, after=after)
        except Exception as e:
            return e
        return

    async def ensure_voice(self, ctx):  # check if the bot is in the same voice channel as the user
        guild_id = ctx.guild.id
        voice = ctx.channel.guild.voice_client
        authorChannel = ctx.author.voice.channel if ctx.author.voice else None
        if authorChannel is None:
            embed = nc.Embed(title="You must be in a voice channel to use this.", color=colors["error"])
            await ctx.send(embed=embed)
            return False
        else:
            if guild_id not in songqueue.keys():
                songqueue[guild_id] = []
            if voice is None:
                await ctx.author.voice.channel.connect()
                embed = nc.Embed(title="Connected to your voice channel.", color=colors["success"])
                await ctx.send(embed=embed)
            elif ctx.author.voice.channel is not voice.channel:
                await voice.move_to(ctx.author.voice.channel)
                embed = nc.Embed(title="Inconsistency in bot's channel, Moved to your voice channel.",
                                 color=colors["neutral"])
                await ctx.send(embed=embed)
            await ctx.guild.change_voice_state(channel=ctx.author.voice.channel, self_mute=False, self_deaf=True)
            return True
        
    def after(self, guildid, err):
        ctx = songqueue[guildid][0][4]
        nxt = QUEUE().next(ctx)
        if nxt is None:
            coro = ctx.send(embed=nc.Embed(title="Song ended.",
                                           description="Queue is empty cannot proceed, add songs using the play/add command",
                                           color=colors["success"]))
        else:
            url, src, title = nxt[0], nxt[1], nxt[3]
            coro = ctx.send(embed=nc.Embed(title="Playing Next", description="**" + title + "**", color=colors[src]))
        fut = asyncio.run_coroutine_threadsafe(coro, self.client.loop)
        if nxt is not None:
            self.player(ctx, url)
        try:
            fut.result()
        except Exception as e:
            print(e)
            pass

    async def play(self, ctx, arg):  # play a song
        if arg == ():
            embed = nc.Embed(title="Please enter a search query.",
                             description="Most music streamings site links are accepted, if otherwise query terms will be considered as youtube search terms",
                             color=0xf54257)
            await ctx.send(embed=embed)
            return
        check = await self.ensure_voice(ctx)
        if check is False:
            return
        guild_id = ctx.guild.id
        voice = ctx.channel.guild.voice_client
        if guild_id not in songqueue.keys():
            songqueue[guild_id] = []
        if voice.is_playing():
            embed = nc.Embed(title="Song already playing, adding to Queue", color=colors["neutral"])
            message = await ctx.send(embed=embed)
            try:
                url, src, thumb, title, ctx = QUEUE().add(ctx, arg)
                embed = nc.Embed(title="Song already playing, added to Queue", description="**" + title + "**",
                                 color=colors[src])
                if src != "fallback":
                    embed.set_footer(text="Powered by odesli & ytdl!")
                embed.set_thumbnail(url=thumb)
                await message.edit(embed=embed)
            except Exception as e:
                embed = nc.Embed(title="Unable to play the song, sorry. :(", description=str(e), color=colors["error"])
                await message.edit(embed=embed)
            return
        try:
            url, src, thumb, title, ctx = QUEUE().add(ctx, arg)
            self.player(ctx, url)
            embed = nc.Embed(title=f"Now Playing: {title}", color=colors[src])
            embed.set_footer(text="Powered by odesli & ytdl!")
            embed.set_thumbnail(url=thumb)
            await ctx.send(embed=embed)
        except Exception as e:
            embed = nc.Embed(title="Unable to find the song, sorry. :(", description="Error:" + str(e), color=colors["error"])
            await ctx.send(embed=embed)
            return
        # song = QUEUE().get_current_song(ctx)
        # try:
        #     url, src, thumb = song[0], song[1], song[2]
            
        # except Exception as e:
        #     embed = nc.Embed(title="An Error Occured", description=e, color=colors["error"])
        #     await ctx.send(embed=embed)
        #     voice.stop()
        #     nxt = QUEUE().next(ctx)
        #     if nxt is None:
        #         await ctx.send(embed=nc.Embed(title="Skipped song.",
        #                                 description="Queue is empty cannot proceed, add songs using the play/add command",
        #                                 color=colors["success"]))
        #     else:
        #         url, src, title = nxt[0], nxt[1], nxt[3]
        #         ctx.send(embed=nc.Embed(title="Skipped song, Playing Next", description="**" + title + "**",
        #                                 color=colors[src]))

    async def skip(self, ctx, position: int = None):  # skip a song
        check = await self.ensure_voice(ctx)
        if check is False:
            return
        voice = ctx.channel.guild.voice_client
        try:
            voice.stop()
            nxt = QUEUE().next(ctx)
            if nxt is None:
                await ctx.send(embed=nc.Embed(title="Skipped song.",
                                              description="Queue is empty cannot proceed, add songs using the play/add command",
                                              color=colors["success"]))
            else:
                url, src, title = nxt[0], nxt[1], nxt[3]
                await ctx.send(embed=nc.Embed(title="Skipped song, Playing Next", description="**" + title + "**",
                                              color=colors[src]))
                self.player(ctx, url)
        except Exception as e:
            ctx.send(embed=nc.Embed(title="An Error Occured whilist trying to skip song", description=e,
                                    color=colors["error"]))
            return

class music(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.p = PLAYER(self.client)

    @commands.command(name="play", aliases=["p", "add", "a"])  # play command
    async def command_play(self, ctx, *arg):
        await self.p.play(ctx, arg)

    @commands.command(name="queue", aliases=["q", "list", "l"])  # list the queue
    async def command_queue(self, ctx):
        guild_id = ctx.guild.id
        if guild_id not in songqueue.keys():
            songqueue[guild_id] = []
        np = QUEUE().now_playing(ctx)
        if np != None:
            description = "**Now playing:** " + np[3]
        else:
            description = ""
        embed = nc.Embed(title="Song Queue", description=description, color=colors["neutral"])
        if len(songqueue[guild_id]) > 1:
            for i in songqueue[guild_id]:
                if i == songqueue[guild_id][0]:
                    continue
                id = songqueue[guild_id].index(i)
                embed.add_field(name=str(id) + ". " + i[3], value=f"`Position {id}`", inline=False)
        else:
            embed.add_field(name="No songs in queue",
                            value="songs are added automatically to queue when there is already a song playing",
                            inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="skip", aliases=["s", "next"])  # skip the current song
    async def command_skip(self, ctx):
        await self.p.skip(ctx)

    @commands.command(name="join", aliases=["j", "connect", "c"])
    async def command_join(self, ctx):
        await self.p.ensure_voice(ctx)

    @commands.command()
    async def dump(self, ctx):
        ctx.send(songqueue)

    @commands.command(name="stop", aliases=["st", "end", "fuckoff"])  # stop the bot from playing music
    async def command_stop(self, ctx):
        voice = ctx.channel.guild.voice_client
        if voice is not None:
            QUEUE().clear(ctx)
            await voice.disconnect()
            embed = nc.Embed(title="Stopped playing music, and cleared song queue", color=colors["success"])
        else:
            embed = nc.Embed(title="Bot not in a voice channel", color=colors["error"])
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):  # checks if there are more than one person in the voice channel or else leaves
        if member.id == self.client.user.id:
            return
        voice = nc.utils.get(self.client.voice_clients, guild=member.guild)
        if voice is None:
            return
        voice_channel = voice.channel
        member_count = len(voice_channel.members)
        if member_count == 1:
            await asyncio.sleep(30)
            if member_count == 1:
                await voice.disconnect()
                guildid = member.guild.id
                ctx = songqueue[guildid][0][4]
                QUEUE().clear(ctx)
                embed = nc.Embed(title="Left voice channel, and cleared queue",
                                 description="No one else in the voice channel :/", color=colors["neutral"])
                await ctx.send(embed=embed)
