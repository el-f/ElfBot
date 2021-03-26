from discord.ext.commands import *
from utils.utils import get_prefix_for_guild_id
import random
from extensions.extension_templates import Extension


class ExtraCommands(Extension):
    @command(aliases=['8ball'], brief="Play a game of 8ball")
    async def _8ball(self, ctx: Context, *, question=None):
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
        pf = get_prefix_for_guild_id(ctx.guild.id)
        await ctx.send(
            f"{ctx.author.mention}\nPlease Enter a Question After '{pf}8ball'\nFor Example: '{pf}8ball are you dumb?'"
            if question is None else
            f'{ctx.author.mention}\nQuestion: {question}\nAnswer: {random.choice(responses)}'
        )


# a simple example of a custom check for a command
def is_creator(ctx: Context):
    return 'elfein' in ctx.author.name.lower()


class AdminCommands(Extension):
    @command(brief="Get the bot's latency")
    async def ping(self, ctx: Context):
        await ctx.send(f'{ctx.author.mention} latency: ({round(self.bot.latency * 1000)}ms)')

    @command(brief="Clear previous messages. Can be called with a specific amount")
    @has_permissions(manage_messages=True)
    async def clear(self, ctx: Context, amount=1):  # default amount - delete last message
        await ctx.channel.purge(limit=amount + 1)  # +1 to delete itself as well

    # Example of Command-Specific Error Handling:
    #
    # @clear.error  # (@command_name.error)
    # async def clear_error(self, ctx, error):
    #     pass

    # an example for a command with a custom check
    @command(hidden=True)
    @check(is_creator)
    async def creator(self, ctx: Context):
        await ctx.send(f'😎 {ctx.author.mention} 😎')

    @command(brief="Link the bot's source code")
    async def repo(self, ctx: Context):
        await ctx.send('Source Code:\nhttps://github.com/Elfein7Night/ElfBot')

    @command(brief="Get an invite link to join the bot to your server")
    async def invite(self, ctx: Context):
        await ctx.send(f'{ctx.author.mention} Invite me to your server here:\nhttps://bit.ly/31cs0qz')

    @command(brief="Get the number of servers the bot is moderating")
    async def deployment(self, ctx: Context):
        await ctx.send(f'{ctx.author.mention}'
                       f' {self.bot.user.name} Is Currently Moderating {len(self.bot.guilds)} Servers')


# expected function for outside calling function 'load_extension()'
def setup(_bot):
    _bot.add_cog(AdminCommands(_bot))
    _bot.add_cog(ExtraCommands(_bot))
