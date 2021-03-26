from discord.ext.commands import Cog, Context, command, has_permissions
from utils.utils import log_event
from extensions.extension_templates import DatabaseHandler


class PrefixDBHandler(DatabaseHandler):
    # On First Joining Server
    @Cog.listener()
    async def on_guild_join(self, guild: Context.guild):
        from utils.utils import DEFAULT_PREFIX
        self.set_value_for_server(guild_id=guild.id, value=DEFAULT_PREFIX)
        log_event(f'Joined the server: {guild.name} - {guild.id}')

    # On Leaving Server
    @Cog.listener()
    async def on_guild_remove(self, guild: Context.guild):
        self.remove_server(guild_id=guild.id)
        log_event(f"left the server '{guild}'")

    @command(brief="Change the bot's prefix for this server")
    @has_permissions(administrator=True)
    async def pf(self, ctx: Context, prefix):
        self.set_value_for_server(guild_id=ctx.guild.id, value=prefix)
        message = f"set '{prefix}' as the prefix for the server '{ctx.guild}'"
        log_event(message)
        await ctx.send(f'{ctx.author.mention} {message}')


# expected function for outside calling function 'load_extension()'
def setup(_bot):
    from utils.utils import PREFIXES_DB_KEY
    _bot.add_cog(PrefixDBHandler(_bot, PREFIXES_DB_KEY))
