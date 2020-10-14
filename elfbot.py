from discord.ext import commands
import discord
import os
import json
import logging
from datetime import datetime

logging.basicConfig(filename='events.log', level=logging.INFO, format="<%(levelname)s> %(message)s")
TOKEN = open("token", "r").read()  # the token is in a private file called "token"
PREFIXES_PATH = 'database/prefixes_for_servers.json'


def get_prefix_from_guild_id(gid):
    prefixes = json.load(open(PREFIXES_PATH, 'r'))
    return prefixes[str(gid)]


def get_prefix(bot, message):  # 'bot' arg is passed but not used
    log_event(f"got an useless arg {bot}")
    return get_prefix_from_guild_id(message.guild.id)


elfbot = commands.Bot(command_prefix=get_prefix)  # callable prefix - invoked on every message


def log_event(string, level=logging.INFO):
    message = f'{datetime.now().strftime("[%d/%m/%y | %H:%M:%S]")} - {string}'
    logging.log(level=level, msg=message)
    print(message)


@elfbot.event
async def on_ready():
    await elfbot.change_presence(activity=discord.Activity(name='for a mention',
                                                           type=discord.ActivityType.watching
                                                           )
                                 )
    log_event(f'{elfbot.user} is Online')


@elfbot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please add required argument to command')
    if isinstance(error, commands.MissingPermissions):
        log_event(f'{ctx.author} tried using a restricted command ({ctx.command})', logging.WARN)
    else:
        log_event(f'An Error Occurred! - [Error: {error} | Command: {ctx.command} | Author: {ctx.author}]',
                  logging.WARN)


@elfbot.event
async def on_message(message):
    if message.author == elfbot.user:
        return
    if elfbot.user.mentioned_in(message):
        pf = get_prefix_from_guild_id(message.guild.id)
        await message.channel.send(f'My prefix in this server is {pf}\nUse "{pf}help" for more info')
    else:
        await elfbot.process_commands(message)


# load all extensions
for filename in os.listdir('extensions'):
    if filename.endswith('.py'):
        elfbot.load_extension(f'extensions.{filename[:-3]}')

elfbot.run(TOKEN)
