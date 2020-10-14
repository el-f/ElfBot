import json
from discord.ext import commands
from utils.utils import log_event, MUSIC_CHANNELS_PATH


def remove_server(gid):
    music_channels = json.load(open(MUSIC_CHANNELS_PATH, 'r'))
    music_channels.pop(str(gid))
    json.dump(music_channels, open(MUSIC_CHANNELS_PATH, 'w'), indent=4)


class MusicChannelsDBHandler(commands.Cog):
    def __init__(self, _bot):
        self.bot = _bot

    @commands.Cog.listener()
    async def on_ready(self):
        log_event(f'{self.qualified_name} extension loaded')

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        remove_server(guild.id)

    @commands.command(brief="Set a text channel to a music spam channel")
    @commands.has_permissions(administrator=True)
    async def setmusic(self, ctx):
        music_channels = json.load(open(MUSIC_CHANNELS_PATH, 'r'))
        music_channels[str(ctx.guild.id)] = ctx.channel.id
        json.dump(music_channels, open(MUSIC_CHANNELS_PATH, 'w'), indent=4)
        message = f"{ctx.channel.name} is now set as the music spam channel for the server '{ctx.guild}'"
        log_event(message)
        await ctx.send(f'{ctx.author.mention} {message}')

    @commands.command(brief="Delete the music spam setting for a server")
    @commands.has_permissions(administrator=True)
    async def delmusic(self, ctx):
        remove_server(ctx.guild.id)
        message = f"music spam settings for the server '{ctx.guild}' have been deleted"
        log_event(message)
        await ctx.send(f'{ctx.author.mention} {message}')


# expected function for outside calling function 'load_extension()'
def setup(_bot):
    _bot.add_cog(MusicChannelsDBHandler(_bot))
