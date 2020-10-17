import json
from discord.ext import commands
from utils.utils import log_event, PREFIXES_DB_KEY, DEFAULT_PREFIX, db


def set_prefix_for_server(guild_id, prefix=DEFAULT_PREFIX):
    if db.get(PREFIXES_DB_KEY) is None:
        prefixes_for_servers = {}
    else:
        prefixes_for_servers = json.loads(db.get(PREFIXES_DB_KEY).decode('utf-8'))

    prefixes_for_servers[str(guild_id)] = prefix
    db.set(PREFIXES_DB_KEY, json.dumps(prefixes_for_servers))


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
        log_event(f"left the server '{guild}'")
        if db.get(PREFIXES_DB_KEY) is not None:
            prefixes_for_servers = json.loads(db.get(PREFIXES_DB_KEY).decode('utf-8'))
            try:
                prefixes_for_servers.pop(str(guild.id))
                db.set(PREFIXES_DB_KEY, json.dumps(prefixes_for_servers))
            except KeyError:
                pass

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
