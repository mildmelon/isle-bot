from discord.ext import commands

from game.game import Game
from game.inventory import Inventory
from game.player import Player
from utils.check import is_private


class GuildCog:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True,
                      description='Join the guild of the current discord server, ' +
                                  'if a name is passed then join that guild instead.')
    async def join(self, context, guild_name=None):
        """ Join a guild. """
        private_channel = is_private(context.message)
        if private_channel and guild_name is None:
            return await self.bot.say('You must enter the name of the guild you would like to join.')

        if private_channel:
            guild = Game.search_guilds(guild_name)
        else:
            guild = Game.get_guild(context.message.server)

        if guild is None:
            return await self.bot.say('That guild does not exist or is not registered.')

        player = Game.get_player(context.message.author)
        if player and player.guild:
            return await self.bot.say(f'You already belong to the guild {player.guild.name}')
        elif player is None:
            # invoke the 'create' command, instead of rewriting functionality
            return await self.bot.commands.get('create').invoke(context)

        await self.bot.say(player.join_guild(guild))

    @commands.command(pass_context=True)
    async def leave(self, context):
        """ Leave your current guild. """
        player = Game.get_player(context.message.author)

        message = player.leave_guild()
        await self.bot.say(message)


def setup(bot):
    bot.add_cog(GuildCog(bot))
