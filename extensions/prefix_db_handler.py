import json
from discord.ext.commands import Cog, Context, command, has_permissions
from utils.utils import log_event, PREFIXES_DB_KEY, DEFAULT_PREFIX, db


def set_prefix_for_server(guild_id: int, prefix=DEFAULT_PREFIX):
    prefixes_raw_dict = db.get(PREFIXES_DB_KEY)
    if prefixes_raw_dict is None:
        prefixes_for_servers = {}
    else:
        prefixes_for_servers = json.loads(prefixes_raw_dict.decode('utf-8'))

    prefixes_for_servers[str(guild_id)] = prefix
    db.set(PREFIXES_DB_KEY, json.dumps(prefixes_for_servers))


class PrefixDBHandler(Cog):
    def __init__(self, _bot):
        self.bot = _bot

    @Cog.listener()
    async def on_ready(self):
        log_event(f'{self.qualified_name} extension loaded')

    # On First Joining Server
    @Cog.listener()
    async def on_guild_join(self, guild: Context.guild):
        set_prefix_for_server(guild.id)
        log_event(f'Joined the server: {guild.name} - {guild.id}')

    # On Leaving Server
    @Cog.listener()
    async def on_guild_remove(self, guild: Context.guild):
        log_event(f"left the server '{guild}'")
        prefixes_raw_dict = db.get(PREFIXES_DB_KEY)
        if prefixes_raw_dict is not None:
            prefixes_for_servers = json.loads(prefixes_raw_dict.decode('utf-8'))
            try:
                prefixes_for_servers.pop(str(guild.id))
                db.set(PREFIXES_DB_KEY, json.dumps(prefixes_for_servers))
            except KeyError:
                pass

    @command(brief="Change the bot's prefix for this server")
    @has_permissions(administrator=True)
    async def pf(self, ctx: Context, prefix):
        set_prefix_for_server(ctx.guild.id, prefix)
        message = f"set '{prefix}' as the prefix for the server '{ctx.guild}'"
        log_event(message)
        await ctx.send(f'{ctx.author.mention} {message}')


# expected function for outside calling function 'load_extension()'
def setup(_bot):
    _bot.add_cog(PrefixDBHandler(_bot))
