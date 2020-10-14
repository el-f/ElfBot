import json
from discord.ext import commands
from utils.utils import log_event, PREFIXES_PATH

DEFAULT_PREFIX = '?'


def set_prefix_for_server(guild_id, prefix=DEFAULT_PREFIX):
    prefixes = json.load(open(PREFIXES_PATH, 'r'))
    prefixes[str(guild_id)] = prefix
    json.dump(prefixes, open(PREFIXES_PATH, 'w'), indent=4)


class PrefixDBHandler(commands.Cog):
    def __init__(self, _bot):
        self.bot = _bot

    @commands.Cog.listener()
    async def on_ready(self):
        log_event(f'{self.qualified_name} extension loaded')

    # On First Joining Server
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        set_prefix_for_server(guild.id)
        log_event(f'Joined the server: {guild.name} - {guild.id}')

    # On Leaving Server
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        prefixes = json.load(open(PREFIXES_PATH, 'r'))
        prefixes.pop(str(guild.id))
        json.dump(prefixes, open(PREFIXES_PATH, 'w'), indent=4)
        log_event(f"Left the server '{guild}'")

    @commands.command(brief="Change the bot's prefix for this server")
    @commands.has_permissions(administrator=True)
    async def pf(self, ctx, prefix):
        set_prefix_for_server(ctx.guild.id, prefix)
        message = f"set '{prefix}' as the prefix for the server '{ctx.guild}'"
        log_event(message)
        await ctx.send(f'{ctx.author.mention} {message}')


# expected function for outside calling function 'load_extension()'
def setup(_bot):
    _bot.add_cog(PrefixDBHandler(_bot))
