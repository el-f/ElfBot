import logging
from discord import Message
from discord.ext.commands import Cog, Context, command, has_permissions
from utils.utils import log_event, db, get_dict
from extensions.extension_templates import DatabaseHandler

DEFAULT_PREFIX = '?'
PREFIXES_DB_KEY = 'prefixes_for_servers'


class PrefixDBHandler(DatabaseHandler):
    # On First Joining Server
    @Cog.listener()
    async def on_guild_join(self, guild: Context.guild):
        self.set_value_for_server(guild_id=guild.id, value=DEFAULT_PREFIX)
        log_event(f'Joined the server: {guild.name} - {guild.id}')

    @command(brief="Change the bot's prefix for this server")
    @has_permissions(administrator=True)
    async def pf(self, ctx: Context, prefix):
        self.set_value_for_server(guild_id=ctx.guild.id, value=prefix)
        message = f"set '{prefix}' as the prefix for the server '{ctx.guild}'"
        log_event(message)
        await ctx.send(f'{ctx.author.mention} {message}')


############################
#      STATIC METHODS      #
############################

def get_prefix_for_guild_id(guild_id: int):
    prefixes_raw_dict = db.get(PREFIXES_DB_KEY)
    if prefixes_raw_dict is not None:
        try:
            return get_dict(prefixes_raw_dict)[str(guild_id)]
        except KeyError:
            log_event(f"Failed trying to fetch prefix for server id {guild_id}", logging.CRITICAL)
            return DEFAULT_PREFIX
    log_event(f"Error Fetching prefixes DB", logging.CRITICAL)
    return DEFAULT_PREFIX


def get_prefix(bot, message: Message):  # bot is passed but not needed (type: commands.Bot)
    return get_prefix_for_guild_id(message.guild.id)


# expected function for outside calling function 'load_extension()'
def setup(_bot):
    _bot.add_cog(PrefixDBHandler(_bot, PREFIXES_DB_KEY))
