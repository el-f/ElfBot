import json
from datetime import datetime
import logging
from discord.message import Message

PREFIXES_PATH = 'database/prefixes_for_servers.json'
MUSIC_CHANNELS_PATH = 'database/music_channels_for_servers.json'

logging.basicConfig(filename='../events.log', level=logging.INFO, format="<%(levelname)s> %(message)s")


def log_event(string, level=logging.INFO):
    msg = f'{datetime.now().strftime("[%d/%m/%y | %H:%M:%S]")} - {string}'
    logging.log(level=level, msg=msg)
    print(msg)


def is_music_related(message: Message):
    author = str(message.author)
    music_bots = [
        'Groovy#7254',
        'Rythm#3722'
    ]
    for bot in music_bots:
        if bot == author:
            return True

    music_related_words = [
        'play',
        'skip',
        'queue',
        'next',
        'loop',
        'resume',
        'pause',
        'p'
    ]
    msg = str(message.content)[1:]
    for word in music_related_words:
        if msg.startswith(word):
            return True

    return False


def in_music_channel(message):
    try:
        return message.channel.id == get_music_channel_for_guild(message.guild.id)
    except KeyError:
        log_event(f"Failed trying to find a music channel for server '{message.guild}'", logging.WARN)
        return True  # if there is no music channel then all channels are music channels


def get_music_channel_for_guild(gid):
    music_channels = json.load(open(MUSIC_CHANNELS_PATH, 'r'))
    return music_channels[str(gid)]


def get_prefix_for_guild(gid):
    prefixes = json.load(open(PREFIXES_PATH, 'r'))
    return prefixes[str(gid)]


def get_prefix(bot, message: Message):  # 'bot' arg is passed but not used
    return get_prefix_for_guild(message.guild.id)
