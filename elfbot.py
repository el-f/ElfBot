import random
from discord.ext import commands

bot = commands.Bot(command_prefix='?')
token = open("token", "r").read()  # the token is in a private file called "token"


@bot.event
async def on_ready():
    print(f'{bot.user} is Online')


@bot.command()
async def ping(ctx):
    await ctx.send(f'WIP 🤫 ({round(bot.latency * 1000)}ms)')


@bot.command(aliases=['8ball'])
async def _8ball(ctx, *, question=None):
    responses = [
        "It is certain.",
        "It is decidedly so.",
        "Without a doubt.",
        "Yes - definitely.",
        "You may rely on it.",
        "As I see it, yes.",
        "Most likely.",
        "Outlook good.",
        "Yes.",
        "Signs point to yes.",
        "Reply hazy, try again.",
        "Ask again later.",
        "Better not tell you now.",
        "Cannot predict now.",
        "Concentrate and ask again.",
        "Don't count on it.",
        "My reply is no.",
        "My sources say no.",
        "Outlook not so good.",
        "Very doubtful."
    ]
    await ctx.send(
        f"Please Enter a Question After '{bot.command_prefix}8ball'" if question is None
        else f'Question: {question}\nAnswer: {random.choice(responses)}'
    )


@bot.command()
@commands.has_permissions(administrator=True)
async def clear(ctx, amount=2):
    await ctx.channel.purge(limit=amount)


bot.run(token)
