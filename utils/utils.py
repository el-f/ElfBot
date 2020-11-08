import json
import os
import redis
from datetime import datetime
import logging
from discord.message import Message

DEFAULT_PREFIX = '?'
PREFIXES_DB_KEY = 'prefixes_for_servers'
MUSIC_CH_DB_KEY = 'music_channels_for_servers'

logging.basicConfig(filename='events.log', level=logging.INFO, format="<%(levelname)s> %(message)s")


def log_event(string, level=logging.INFO):
    msg = f'{datetime.now().strftime("[%d/%m/%y | %H:%M:%S]")} - {string}'
    logging.log(level=level, msg=msg)
    print(msg)


def get_db_url():
    """
    the db_url is in a private file called "db_url"
    first we try to find the token file for case of running from individual machine
    if file not found we look for environment var for case of running from a deployed server
    :return: db_url (string)
    """
    try:
        db_url = open("utils/db_url", "r").read()
        log_event('Fetched db_url from db_url file')
        return db_url
    except FileNotFoundError:
        log_event('Fetched db_url from environment variable')
        return os.getenv('REDISTOGO_URL', 'redis://localhost:6379')


db = redis.from_url(get_db_url())


def get_token():
    """
    the token is in a private file called "token"
    first we try to find the token file for case of running from individual machine
    if file not found we look for environment var for case of running from a deployed server
    :return: token (string)
    """
    try:
        token = open("utils/token", "r").read()
        log_event('Fetched token from token file')
        return token
    except FileNotFoundError:
        log_event('Fetched token from environment variable')
        return os.getenv('DISCORD_BOT_TOKEN')


def is_music_related(message: Message):
    help_command_trigger = 'list of commands'
    # for case of 'help' command
    if message.embeds:
        for embed in message.embeds:
            if help_command_trigger in embed.description:
                return False
            if embed.fields:
                for field in embed.fields:
                    if help_command_trigger in str(field):
                        return False

    author = str(message.author)
    music_bots = [
        # top 5 most used music bots
        'Groovy#7254',
        'Rythm#3722',
        'FredBoat♪♪#7284',
        '24/7 🔊#6493',
        'Vexera#8487'
    ]
    for bot in music_bots:
        if author == bot:
            return True

    msg = str(message.content)[1:].lower()
    music_related_commands = [
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


def get_music_channel_id_for_guild_id(guild_id):
    if db.get(MUSIC_CH_DB_KEY) is None:
        raise KeyError

    music_channels = json.loads(db.get(MUSIC_CH_DB_KEY).decode('utf-8'))
    return music_channels[str(guild_id)]


def get_prefix_for_guild_id(guild_id):
    if db.get(PREFIXES_DB_KEY) is not None:
        try:
            prefixes = json.loads(db.get(PREFIXES_DB_KEY).decode('utf-8'))
            return prefixes[str(guild_id)]
        except KeyError:
            log_event(f"Failed trying to fetch prefix for server id {guild_id}", logging.CRITICAL)
            return DEFAULT_PREFIX
    log_event(f"Error Fetching prefixes DB", logging.CRITICAL)
    return DEFAULT_PREFIX


def get_prefix(bot, message: Message):  # 'bot' arg is passed but not used
    return get_prefix_for_guild_id(message.guild.id)
