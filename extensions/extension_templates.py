import json
from discord.ext.commands import Cog
from utils.utils import log_event, db, get_dict


class Extension(Cog):
    def __init__(self, _bot):
        self.bot = _bot

    @Cog.listener()
    async def on_ready(self):
        log_event(f'{self.qualified_name} extension loaded')


class DatabaseHandler(Extension):
    def __init__(self, _bot, db_key):
        super().__init__(_bot)
        self.DB_KEY = db_key

    def set_value_for_server(self, guild_id, value):
        raw_dict = db.get(self.DB_KEY)
        if raw_dict is None:
            dictionary = {}
        else:
            dictionary = get_dict(raw_dict)

        dictionary[str(guild_id)] = value
        db.set(self.DB_KEY, json.dumps(dictionary))

    def remove_server(self, guild_id: int):
        raw_dict = db.get(self.DB_KEY)
        if raw_dict is not None:
            dictionary = get_dict(raw_dict)
            try:
                dictionary.pop(str(guild_id))
                db.set(self.DB_KEY, json.dumps(dictionary))
            except KeyError:
                pass
