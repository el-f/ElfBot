from discord.ext import commands
from utils.utils import is_music_related, log_event, get_prefix, get_prefix_for_guild_id, in_music_channel, \
    get_music_channel_id_for_guild_id
import discord
import os
import logging

TOKEN = open("token", "r").read()  # the token is in a private file called "token"

elfbot = commands.Bot(command_prefix=get_prefix)  # callable prefix - invoked on every message


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
        await ctx.send(f'Please use the command with the required argument: <{error.param}>')

    elif isinstance(error, commands.MissingPermissions):
        log_event(f'{ctx.author} tried using a restricted command ({ctx.command})', logging.WARN)
        await ctx.send(f"{ctx.author.mention} you don't have enough permissions to use {ctx.command}")

    else:
        log_event(f'An Error Occurred! - [Error: {error} | Command: {ctx.command} | Author: {ctx.author}]',
                  logging.WARN)


@elfbot.event
async def on_message(message):
    if message.author == elfbot.user:
        return

    if elfbot.user.mentioned_in(message):
        pf = get_prefix_for_guild_id(message.guild.id)
        author = message.author
        await message.channel.send(f'{author.mention}\nMy prefix in this server is {pf}\nUse "{pf}help" for more info')

    elif message and not in_music_channel(message) and is_music_related(message):
        log_event(f'Caught unauthorized music related message: {message.content} by {message.author}')
        music_channel = elfbot.get_channel(get_music_channel_id_for_guild_id(message.guild.id))
        await message.delete()
        if message.embeds:
            for embed in message.embeds:
                await music_channel.send(embed=embed)
        else:
            await music_channel.send(message.content)

    else:
        await elfbot.process_commands(message)


if __name__ == '__main__':
    # load all extensions
    for filename in os.listdir('extensions'):
        if filename.endswith('.py'):
            elfbot.load_extension(f'extensions.{filename[:-3]}')

    elfbot.run(TOKEN)
