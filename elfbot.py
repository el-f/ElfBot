from discord.ext.commands import Bot, Context, MissingRequiredArgument, MissingPermissions, CommandNotFound
from discord import Activity, ActivityType, Message
from extensions.music_handler import process_msg_for_music
from extensions.prefix_handler import get_prefix, get_prefix_for_guild
from utils.utils import *

elfbot = Bot(command_prefix=get_prefix)  # callable prefix - invoked on every message


@elfbot.event
async def on_ready():
    await elfbot.change_presence(
        activity=Activity(type=ActivityType.watching, name='for music spam 👀')
    )
    log_event(f'{elfbot.user} is Online')


@elfbot.event
async def on_command_error(ctx: Context, error):
    if isinstance(error, CommandNotFound):
        return

    if isinstance(error, MissingRequiredArgument):
        await ctx.send(f'Please use the command with the required argument: <{error.param}>')

    elif isinstance(error, MissingPermissions):
        log_event(f"<server='{ctx.guild}'> {ctx.author} tried using a restricted command ({ctx.command})", logging.WARN)
        await ctx.send(f"{ctx.author.mention} you don't have enough permissions to use {ctx.command}")

    else:
        log_event(f"<server='{ctx.guild}'> An Error Occurred! - [Error: {error} | Command: {ctx.command} |"
                  f" Author: {ctx.author}]", logging.CRITICAL)


@elfbot.event
async def on_message(message: Message):
    if message is None:
        return

    if message.author == elfbot.user:
        return

    if not message.guild:  # DM case
        return

    if elfbot.user.mentioned_in(message):
        pf = get_prefix_for_guild(message.guild.id)
        author = message.author
        await message.channel.send(f'{author.mention}\nMy prefix in this server is {pf}\nUse "{pf}help" for more info')
        return

    if await process_msg_for_music(message, elfbot):
        return

    await elfbot.process_commands(message)


# load all extensions
for filename in os.listdir('extensions'):
    if filename.endswith('.py') and 'template' not in filename:
        elfbot.load_extension(f'extensions.{filename[:-3]}')

elfbot.run(get_token())
