from utils.utils import log_event
import os
import redis


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
        return os.getenv('REDIS_URL', 'redis://localhost:6379')


db = redis.from_url(get_db_url())
