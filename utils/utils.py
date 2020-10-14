import json
from datetime import datetime
import logging
from discord.message import Message

DEFAULT_PREFIX = '?'
PREFIXES_PATH = 'database/prefixes_for_servers.json'
MUSIC_CHANNELS_PATH = 'database/music_channels_for_servers.json'

logging.basicConfig(filename='../events.log', level=logging.INFO, format="<%(levelname)s> %(message)s")


def log_event(string, level=logging.INFO):
    msg = f'{datetime.now().strftime("[%d/%m/%y | %H:%M:%S]")} - {string}'
    logging.log(level=level, msg=msg)
    print(msg)


def is_music_related(message: Message):
    help_command_trigger = 'list of commands'
    # for case of 'help' command
    if message.embeds:
        for embed in message.embeds:
            if help_command_trigger in embed.description:
                return False
            elif embed.fields:
                for field in embed.fields:
                    if help_command_trigger in str(field):
                        return False

    author = str(message.author)
    music_bots = [
        'Groovy#7254',
        'Rythm#3722'
    ]
    for bot in music_bots:
        if author == bot:
            return True

    music_related_commands = [
        'play',
        'skip',
        'queue',
        'next',
        'loop',
        'resume',
        'pause',
        'p',
        'fs',
        'lyrics'
    ]
    msg = str(message.content)[1:]
    for command in music_related_commands:
        if msg.startswith(command):
            return True

    return False


def in_music_channel(message):
    try:
        return message.channel.id == get_music_channel_id_for_guild_id(message.guild.id)
    except KeyError:
        log_event(f"Failed trying to find a music channel for server '{message.guild}'", logging.WARN)
        return True  # if there is no music channel then all channels are music channels


def get_music_channel_id_for_guild_id(gid):
    music_channels = json.load(open(MUSIC_CHANNELS_PATH, 'r'))
    return music_channels[str(gid)]


def get_prefix_for_guild_id(gid):
    try:
        prefixes = json.load(open(PREFIXES_PATH, 'r'))
        return prefixes[str(gid)]
    except KeyError:
        return DEFAULT_PREFIX


def get_prefix(bot, message: Message):  # 'bot' arg is passed but not used
    return get_prefix_for_guild_id(message.guild.id)
