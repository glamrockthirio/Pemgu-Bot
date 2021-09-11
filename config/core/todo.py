import discord
from discord.ext import commands

class Todo(commands.Cog, description="Lazy people use these"):
    def __init__(self, bot):
        self.bot = bot

    # Todo
    @commands.group(name="todo", help="Will show your todo list", invoke_without_command=True)
    async def todo(self, ctx):
        await ctx.trigger_typing()
        tasks = await self.bot.db.fetch("SELECT task FROM todos WHERE user_id = $1", ctx.author.id)
        if len(tasks) == 0:
            await ctx.send("You don't have a todo list\nTry to make one with `todo add` command")
        else:
            todombed = discord.Embed(
                colour=self.bot.color,
                title="Here is your todo list",
                timestamp=ctx.message.created_at
            )
            todombed.description = "\n".join(f"{i+1} {task['task']}" for i, task in enumerate(tasks))
            todombed.set_footer(text=ctx.author, icon_url=ctx.author.avatar.url)
            await ctx.send(embed=todombed)

    # Add
    @todo.command(name="add", help="Will add the given task", usage="<task>")
    async def add(self, ctx, *, text):
        await ctx.trigger_typing()
        await self.bot.db.execute("INSERT INTO todos(user_id, task) VALUES($1, $2)", ctx.author.id, text)
        await ctx.send(F"`{text}` has been added")

    # Remove
    @todo.command(name="remove", help="Will remove the given task", usage="<task>")
    async def remove(self, ctx, *, text):
        await ctx.trigger_typing()
        task = await self.bot.db.fetch(F"SELECT task FROM todos WHERE user_id = $1 AND task = $2", ctx.author.id, text)
        if len(task) == 0:
            await ctx.send(F"You don't have `{text}` in your list")
        else:
            await self.bot.db.execute("DELETE FROM todos WHERE user_id = $1 AND task = $2", ctx.author.id, text)
            await ctx.send(F"`{text}` has been removed")

def setup(bot):
    bot.add_cog(Todo(bot))