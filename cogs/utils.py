if __name__ == "__main__":
    print("This is a cog, execute main.py!")
    exit()

# supress sklearns annoying warnings
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

from inspect import getsource  # for eval
import nextcord as nc  # nc for discord, json for loading settings
import json, os, sys
from time import time
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
from profanity_check import predict_prob  # for profanity filter

# import settings from settings.json
vardb = json.load(open("settings.json"))


# setup
def setup(client):
    client.add_cog(utils(client))


class utils(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)  # load unload cogs for debugging purposes
    async def sudo(self, ctx, *arg):
        if ctx.message.author.id != vardb["owner_id"]:
            await ctx.send("Access Denied")
            return
        if arg[0] == "cog":
            if arg[1] == "reload":
                try:
                    cog = "cogs." + arg[2]
                    self.client.reload_extension(cog)
                    await ctx.send("Reloaded `" + arg[2] + "` Successfully")
                except Exception as e:
                    await ctx.send("Error: " + str(e))
            elif arg[1] == "unload":
                try:
                    cog = "cogs." + arg[2]
                    self.client.unload_extension(cog)
                    await ctx.send("Unloaded `" + arg[2] + "` Successfully")
                except Exception as e:
                    await ctx.send("Error: " + str(e))
            elif arg[1] == "load":
                try:
                    cog = "cogs." + arg[2]
                    self.client.load_extension(cog)
                    await ctx.send("Loaded `" + arg[2] + "` Successfully")
                except Exception as e:
                    await ctx.send("Error: " + str(e))
            else:
                await ctx.send("Usage: sudo cog <command> <arg>, where command is one of: reload, unload, load")
        elif arg[0] == "profcheck":
            if arg[1].lower() in ["add", "enable", "on"]:
                # todo
                return
            elif arg[1].lower() in ["remove", "disable", "off"]:
                # todo
                return
            else:
                ctx.send("Usage: sudo profcheck <arg>, where command is one of: add, remove")
                return
        else:
            await ctx.send("Usage: sudo <command>, where command is one of: cog, profcheck")
            return

    # Eval Helpers
    # Code shamelessly stolen from https://gist.github.com/vierofernando/c5796a78292b949341c98a5deaee8eda since my pea brain cant comprehend this stuff

    def resolve_variable(self, variable):
        if hasattr(variable, "__iter__"):
            var_length = len(list(variable))
            if (var_length > 100) and (not isinstance(variable, str)):
                return f"<a {type(variable).__name__} iterable with more than 100 values ({var_length})>"
            elif (not var_length):
                return f"<an empty {type(variable).__name__} iterable>"

        if (not variable) and (not isinstance(variable, bool)):
            return f"<an empty {type(variable).__name__} object>"
        return (variable if (
                len(f"{variable}") <= 1000) else f"<a long {type(variable).__name__} object with the length of {len(f'{variable}'):,}>")

    def prepare(self, string):
        arr = string.strip("```").replace("py\n", "").replace("python\n", "").split("\n")
        if not arr[::-1][0].replace(" ", "").startswith("return"):
            arr[len(arr) - 1] = "return " + arr[::-1][0]
        return "".join(f"\n\t{i}" for i in arr)

    @commands.command()
    async def eval(self, ctx, *, code: str):
        if ctx.message.author.id != vardb["owner_id"]:
            await ctx.send("Access Denied")
            return
        silent = ("-s" in code)

        code = self.prepare(code.replace("-s", ""))
        args = {
            "nextcord": nc,
            "sauce": getsource,
            "sys": sys,
            "os": os,
            "imp": __import__,
            "this": self,
            "ctx": ctx
        }

        try:
            exec(f"async def func():{code}", args)
            a = time()
            response = await eval("func()", args)
            if silent or (response is None) or isinstance(response, nc.Message):
                del args, code
                return

            await ctx.send(
                f"```py\n{self.resolve_variable(response)}````{type(response).__name__} | {(time() - a) / 1000} ms`")
        except Exception as e:
            await ctx.send(f"Error occurred:```\n{type(e).__name__}: {str(e)}```")

        del args, code, silent

    @commands.command(pass_context=True)  # purge command for deleting messages
    @commands.has_permissions(administrator=True)
    async def purge(self, ctx, limit: int):
        try:
            await ctx.channel.purge(limit=limit)
            await ctx.send('Cleared by {}'.format(ctx.author.mention), delete_after=3)
        except:
            await ctx.send('Unknown Error, perhaps check permissions?')

    # @nc.slash_command( # Discord api doesnt have a proper permission system for slash commands
    #     name="purge",
    #     description="Purge chat content",
    #     default_permission=False
    # )
    # async def slash_purge(self,interaction:Interaction,limit:int):
    #     await interaction.channel.purge(limit=limit)
    #     await interaction.response.send_message('Cleared by {}'.format(interaction.user.mention),delete_after=3)

    @nc.slash_command(  # change bot status
        name="status",
        description="Set bot status!")
    async def status(self, interaction: Interaction,
                     type: str = SlashOption(
                         name="type",
                         description="Choose status type, i.e Listening, Watching... etc",
                         choices={"watching": "Watching", "listening": "Listening", "playing": "Playing",
                                  "streaming": "Streaming"},
                         required=True),
                     status: str = SlashOption(
                         name="status",
                         description="Set the bot Status",
                         required=True)
                     ):
        embed = nc.Embed(description=f"{type} {status}", title="Setting Status to")  # create embed
        if type == "Listening":
            try:
                await self.client.change_presence(
                    activity=nc.Activity(type=nc.ActivityType.listening, name=f"{status}"))
                await interaction.response.send_message(embed=embed)
            except:
                await interaction.response.send_message("An error occured")
        elif type == "Watching":
            try:
                await self.client.change_presence(activity=nc.Activity(type=nc.ActivityType.watching, name=f"{status}"))
                await interaction.response.send_message(embed=embed)
            except:
                await interaction.response.send_message("An error occured")
        elif type == "Playing":
            try:
                await self.client.change_presence(activity=nc.Activity(activity=nc.Game(name=f"{status}")))
                await interaction.response.send_message(embed=embed)
            except:
                await interaction.response.send_message("An error occured")
        elif type == "Streaming":
            try:
                await self.client.change_presence(activity=nc.Streaming(name=f"{status}",
                                                                        url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"))  # you know where the link leads(hopefully)
                await interaction.response.send_message(embed=embed)
            except:
                await interaction.response.send_message("An error occured")
        else:
            return

    @nc.slash_command(name="ping",  # Ping command
                      description="Ping pong and view latency",
                      )
    async def ping(self, interaction: Interaction):
        embed = nc.Embed(title="Pong! 🏓")
        await interaction.response.send_message(embed=embed)  # reply with embed
        ping = round(self.client.latency * 1000)
        embed.set_footer(text=f"{ping} ms")
        await interaction.edit_original_message(embed=embed)  # edit embed with latency for fanciness

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:  # if message is from bot ignore
            return
        whitelisted_ids = vardb["profCheck"].keys()  # get whitelisted ids
        if str(message.guild.id) in whitelisted_ids and "damn" not in message.content:  # check if guild is whitelisted
            msg_predict_prob = predict_prob([str(message.content)])[0] * 100
            # await message.channel.send("this message has a probability of " + str(msg_predict_prob)+ "% , containing profanity")
            if int(msg_predict_prob) > 82:  # if message contains profanity
                await message.delete()
                channel = self.client.get_channel(vardb["profCheck"][str(message.guild.id)])  # get log channel
                if channel is not None:
                    embed = nc.Embed(title="Message Deleted",
                                     description=f"{message.author.mention} has been deleted for containing a profanity of {msg_predict_prob}%")
                    embed.add_field(name="Message Content:", value=message.content)
                    await channel.send(embed=embed)
                return
