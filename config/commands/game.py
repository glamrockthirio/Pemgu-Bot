import discord
from discord.ext import commands
from config.views import tictactoe, guess

class Game(commands.Cog, description="If you are bored... use these"):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="tictactoe", aliases=["ttt"], help="Will start an tic-tac-toe game")
    @commands.is_owner()
    async def tictactoe(self, ctx):
        await ctx.trigger_typing()
        await ctx.send('Tic Tac Toe: X goes first', view=tictactoe.TicTacToeView())
    
    @commands.command(name="guess", aliases=["gs"], help="Will start an guessing game")
    async def guess(self, ctx):
        await ctx.trigger_typing()
        gsmbed = discord.Embed(
            colour=self.bot.color,
            title="Started the game",
            description="Try to guess now"
        )
        gsmbed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
        view = guess.GuessView(client=self.bot)
        view.message = await ctx.send(view=view)

def setup(bot):
    bot.add_cog(Game(bot))