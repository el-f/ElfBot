from discord.ext.commands import Cog, Context, command, has_permissions
from utils.utils import log_event
from extensions.extension_templates import DatabaseHandler


class MusicChannelsDBHandler(DatabaseHandler):
    @Cog.listener()
    async def on_guild_remove(self, guild: Context.guild):
        self.remove_server(guild_id=guild.id)
        log_event(f"left the server '{guild}'")

    @command(brief="Set a text channel to a music spam channel")
    @has_permissions(administrator=True)
    async def setmusic(self, ctx: Context):
        self.set_value_for_server(ctx.guild.id, ctx.channel.id)
        message = f"'{ctx.channel.name}' is now set as the music spam channel for the server '{ctx.guild}'"
        log_event(message)
        await ctx.send(f'{ctx.author.mention} {message}')

    @command(brief="Delete the music spam setting for a server")
    @has_permissions(administrator=True)
    async def delmusic(self, ctx: Context):
        self.remove_server(guild_id=ctx.guild.id)
        event = f"Music spam settings for the server '{ctx.guild}' have been deleted"
        log_event(event)
        await ctx.send(f'{ctx.author.mention} {event}')


# expected function for outside calling function 'load_extension()'
def setup(_bot):
    from utils.utils import MUSIC_CH_DB_KEY
    _bot.add_cog(MusicChannelsDBHandler(_bot, MUSIC_CH_DB_KEY))
