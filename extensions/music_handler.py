import logging
from discord import Message
from discord.ext.commands import Context, command, has_permissions
from utils.utils import log_event, db, get_dict
from extensions.extension_templates import DatabaseHandler

MUSIC_CH_DB_KEY = 'music_channels_for_servers'


class MusicChannelsDBHandler(DatabaseHandler):
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


#####################
#      STATICS      #
#####################

MUSIC_BOTS = [
    # top 5 most used music bots
    'Groovy#7254',
    'Rythm#3722',
    'FredBoat♪♪#7284',
    '24/7 🔊#6493',
    'Vexera#8487'
]

MUSIC_RELATED_COMMANDS = [
    'play',
    'skip',
    'queue',
    'next',
    'loop',
    'resume',
    'pause',
    'p ',
    'fs',
    'lyrics',
    'stop',
    'join',
    'leave',
    'search',
    'shuffle',
    'seek',
    'np',
    'repeat',
    'previous',
    'replay',
    'volume'
]

HELP_COMMAND_TRIGGER = 'list of commands'


def is_music_related(message: Message):
    # for case of 'help' command
    if message.embeds:
        for embed in message.embeds:
            if HELP_COMMAND_TRIGGER in embed.description:
                return False
            if embed.fields:
                for field in embed.fields:
                    if HELP_COMMAND_TRIGGER in str(field):
                        return False

    author = str(message.author)
    for bot in MUSIC_BOTS:
        if author == bot:
            return True

    msg = str(message.content)[1:].lower()  # remove prefix, insure case matching
    for cmd in MUSIC_RELATED_COMMANDS:
        if msg.startswith(cmd):
            return True

    return False


def in_music_channel(message: Message):
    try:
        return message.channel.id == get_music_channel_id_for_guild_id(message.guild.id)
    except KeyError:
        log_event(f"Failed trying to find a music channel for server '{message.guild}'", logging.WARN)
        return True  # if there is no music channel then all channels are music channels


def get_music_channel_id_for_guild_id(guild_id: int):
    music_channels_raw_dict = db.get(MUSIC_CH_DB_KEY)
    if music_channels_raw_dict is None:
        raise KeyError

    return get_dict(music_channels_raw_dict)[str(guild_id)]


# expected function for outside calling function 'load_extension()'
def setup(_bot):
    _bot.add_cog(MusicChannelsDBHandler(_bot, MUSIC_CH_DB_KEY))
