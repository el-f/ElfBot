import json
import os
import redis
import logging
from datetime import datetime

EVENTS_LOG_FILE_NAME = 'events.log'
logging.basicConfig(filename=EVENTS_LOG_FILE_NAME, level=logging.INFO, format="<%(levelname)s> %(message)s")


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


def get_bool(flag: str) -> bool:
    """
    Get boolean from a string.

    "true" / "t" / "y" -> True

    "false" / "f" / "n" -> False

    :param flag: a string representing a boolean
    :return: boolean
    """
    flag = flag.lower()
    if flag in {"true", "t", "y"}:
        return True
    elif flag in {"false", "f", "n"}:
        return False
    raise ValueError
