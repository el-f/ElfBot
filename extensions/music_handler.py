import logging
from discord import Message
from discord.ext.commands import Context, command, has_permissions, Bot

from extensions import commands
from utils.utils import log_event, db, get_dict, get_bool
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

    @command(brief="Toggle special cases checking in music detection", hidden=True)
    @commands.is_owner()
    async def tsc(self, ctx: Context, flag: str = ""):
        global CHECK_SPECIAL_CASES
        await ctx.message.delete()
        if len(flag) > 0:
            try:
                CHECK_SPECIAL_CASES = get_bool(flag)
            except ValueError:
                await ctx.author.send(f"Invalid Flag Value: {flag}")
        await ctx.author.send(f"CHECK_SPECIAL_CASES now set as {CHECK_SPECIAL_CASES}")


#####################
#      STATICS      #
#####################

MUSIC_BOTS = {
    # top 5 most used music bots
    'Groovy#7254',
    'Rythm#3722',
    'FredBoat♪♪#7284',
    '24/7 🔊#6493',
    'Vexera#8487'
}

MUSIC_RELATED_COMMANDS = {
    'announce',
    'back',
    'clear',
    'dc',
    'disconnect',
    'ff',
    'fs',
    'fwd',
    'goto',
    'join',
    'jump',
    'leave',
    'loop',
    'lyrics',
    'move',
    'next',
    'np',
    'pause',
    'pf',
    'play',
    'prev',
    'previous',
    'queue',
    'remove',
    'repeat',
    'replay',
    'reset',
    'resume',
    'rewind',
    'rr',
    'search',
    'seek',
    'shuffle',
    'skip',
    'song',
    'stop',
    'unpause',
    'volume',
}

# special because of whitespace / multiple words, can't be in the set in a well implemented way
# so we check one by one.
MUSIC_RELATED_SPECIALS_CASES = [
    'fast forward',
    'j ',
    'm ',
    'mv ',
    'p ',
    'q ',
    'rw ',
    's ',
]

CHECK_SPECIAL_CASES = True

HELP_COMMAND_TRIGGER = 'list of commands'


async def process_msg_for_music(message: Message, elfbot: Bot):
    if is_music_related(message) and not in_music_channel(message):
        await message.delete()
        log_event(f"<server='{message.guild}'> Caught unauthorized music related message by {message.author}")
        music_channel = elfbot.get_channel(get_music_channel_id_for_guild(message.guild.id))
        if message.embeds:
            for embed in message.embeds:
                await music_channel.send(embed=embed)
        if message.content:
            await music_channel.send(message.content)
        return True

    return False


def is_music_related(message: Message):
    # for case of 'help' command
    if message.embeds:
        for embed in message.embeds:
            if embed.description and HELP_COMMAND_TRIGGER in embed.description:
                return False
            if embed.fields:
                for field in embed.fields:
                    if HELP_COMMAND_TRIGGER in str(field):
                        return False

    if str(message.author) in MUSIC_BOTS:
        return True

    msg = message.content[1:].lower()  # remove prefix, insure case matching

    # get first string
    if msg.split()[0] in MUSIC_RELATED_COMMANDS:
        return True

    if CHECK_SPECIAL_CASES:
        for sp in MUSIC_RELATED_SPECIALS_CASES:
            if msg.startswith(sp):
                return True

    return False


def in_music_channel(message: Message):
    try:
        return message.channel.id == get_music_channel_id_for_guild(message.guild.id)
    except KeyError:
        log_event(f"Failed trying to find a music channel for server '{message.guild}'", logging.WARN)
        return True  # if there is no music channel then all channels are music channels


def get_music_channel_id_for_guild(guild_id: int):
    music_channels_raw_dict = db.get(MUSIC_CH_DB_KEY)
    if music_channels_raw_dict is None:
        raise KeyError

    return get_dict(music_channels_raw_dict)[str(guild_id)]


# expected function for outside calling function 'load_extension()'
def setup(_bot):
    _bot.add_cog(MusicChannelsDBHandler(_bot, MUSIC_CH_DB_KEY))
