import json
from discord.ext import commands
from utils.utils import log_event, MUSIC_CHANNELS_PATH


class MusicChannelsDBHandler(commands.Cog):
    def __init__(self, _bot):
        self.bot = _bot

    @commands.Cog.listener()
    async def on_ready(self):
        log_event(f'{self.qualified_name} extension loaded')

    @commands.command(brief="Set a text channel to a music spam channel")
    @commands.has_permissions(administrator=True)
    async def setmusic(self, ctx):
        music_channels = json.load(open(MUSIC_CHANNELS_PATH, 'r'))
        music_channels[str(ctx.guild.id)] = ctx.channel.id
        json.dump(music_channels, open(MUSIC_CHANNELS_PATH, 'w'), indent=4)
        await ctx.send(f'{ctx.author.mention} {ctx.channel.name} is now set as the music spam channel for this server')

    @commands.command(brief="Delete the music spam setting for a server")
    @commands.has_permissions(administrator=True)
    async def delmusic(self, ctx):
        music_channels = json.load(open(MUSIC_CHANNELS_PATH, 'r'))
        music_channels.pop(str(ctx.guild.id))
        json.dump(music_channels, open(MUSIC_CHANNELS_PATH, 'w'), indent=4)
        await ctx.send(f'{ctx.author.mention} music spam settings for this server have been deleted')


# expected function for outside calling function 'load_extension()'
def setup(_bot):
    _bot.add_cog(MusicChannelsDBHandler(_bot))
