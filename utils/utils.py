import json
import os
import redis
import logging
from datetime import datetime
from discord.message import Message

###################################
# CONSTANTS + CONFIG + UTIL FUNCS #
###################################

DEFAULT_PREFIX = '?'
PREFIXES_DB_KEY = 'prefixes_for_servers'
MUSIC_CH_DB_KEY = 'music_channels_for_servers'

logging.basicConfig(filename='events.log', level=logging.INFO, format="<%(levelname)s> %(message)s")


def log_event(description: str, level=logging.INFO):
    msg = f'{datetime.now().strftime("[%d/%m/%y | %H:%M:%S]")} - {description}'
    logging.log(level=level, msg=msg)
    print(msg)


def get_db_url():
    """
    the db_url is in a private file called "db_url"
    first we try to find the token file for case of running from individual machine
    if file not found we look for environment var for case of running from a deployed server

    :return: redis db_url (string)
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

    :return: discord user token (string)
    """
    try:
        token = open("utils/token", "r").read()
        log_event('Fetched token from token file')
        return token
    except FileNotFoundError:
        log_event('Fetched token from environment variable')
        return os.getenv('DISCORD_BOT_TOKEN')


def get_dict(raw_json: bytes) -> dict:
    """
    In the database our dictionaries are stored as raw bytes,
    this function returns them decoded and transformed back as dictionaries.

    :param raw_json: A JSON represented as raw bytes string
    :return: A dictionary from the decoded bytes
    """
    return json.loads(raw_json.decode('utf-8'))


#############################
#       MUSIC HANDLING      #
#############################

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
    for command in MUSIC_RELATED_COMMANDS:
        if msg.startswith(command):
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


############################
#      PREFIX HANDLING     #
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
