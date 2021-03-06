import discord, io, textwrap, contextlib, traceback
from discord.ext import commands

class Owner(commands.Cog, description="Only my Developer can use these!"):
    def __init__(self, bot):
        self.bot = bot

    # Eval
    @commands.command(name="eval", help="Evaluates a code")
    @commands.is_owner()
    async def _eval(self, ctx, *, body:str):
        env = {
            "self": self,
            "discord": discord,
            "bot": self.bot,
            "ctx": ctx,
            "message": ctx.message,
            "author": ctx.author,
            "guild": ctx.guild,
            "channel": ctx.channel,
        }
        env.update(globals())
        if body.startswith("```") and body.endswith("```"):
            body = "\n".join(body.split("\n")[1:-1])
        body = body.strip("` \n")
        stdout = io.StringIO()
        to_compile = f"async def func():\n{textwrap.indent(body, '  ')}"
        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f"```py\n{e.__class__.__name__}: {e}\n```")
        func = env["func"]
        try:
            with contextlib.redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f"```py\n{value}{traceback.format_exc()}\n```")
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction("\u2705")
            except:
                pass
            if ret is None:
                if value:
                    await ctx.send(f"```py\n{value}\n```")
            else:
                await ctx.send(f"```py\n{value}{ret}\n```")

    # Load
    @commands.command(name="load", help="Will load the given cog")
    @commands.is_owner()
    async def load(self, ctx:commands.Context, *, cog:str):
        loadmbed = discord.Embed(
            color=self.bot.color,
            title=F"Successfully loaded {cog}.",
            timestamp=ctx.message.created_at
        )
        loadmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        self.bot.load_extension(cog)
        await ctx.send(embed=loadmbed)

    # Unload
    @commands.command(name="unload", help="Will unload the given cog")
    @commands.is_owner()
    async def unload(self, ctx:commands.Context, *, cog:str):
        unloadmbed = discord.Embed(
            color=self.bot.color,
            title=F"Successfully unloaded {cog}.",
            timestamp=ctx.message.created_at
        )
        unloadmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        self.bot.unload_extension(cog)
        await ctx.send(embed=unloadmbed)
  
    # Reload
    @commands.command(name="reload", help="Will reload the given or every cog")
    @commands.is_owner()
    async def reload(self, ctx:commands.Context, *, cog:str=None):
        reloadmbed = discord.Embed(
            color=self.bot.color,
            timestamp=ctx.message.created_at
        )
        if not cog:
            reloadmbed.title = "Successfully reloaded every cog"
            reloadmbed.description = ""
            reloadmbed.description += F"<:greyTick:596576672900186113> Commands:\n"
            for command in self.bot._commands:
                try:
                    self.bot.reload_extension(F"core.commands.{command}")
                    reloadmbed.description += F"<:greenTick:596576670815879169> - {command}\n"
                except Exception as error:
                    reloadmbed.description += F"<:redTick:596576672149667840> - {command}\n"
                    reloadmbed.description += F"<:redTick:596576672149667840> - {error}\n"
            reloadmbed.description += F"<:greyTick:596576672900186113> Events:\n"
            for event in self.bot._events:
                try:
                    self.bot.reload_extension(F"core.events.{event}")
                    reloadmbed.description += F"<:greenTick:596576670815879169> - {event}\n"
                except Exception as error:
                    reloadmbed.description += F"<:redTick:596576672149667840> - {event}\n"
                    reloadmbed.description += F"<:redTick:596576672149667840> - {error}\n"
            return await ctx.send(embed=reloadmbed)
        reloadmbed.title = F"Successfully reloaded {cog}."
        self.bot.reload_extension(cog)
        await ctx.send(embed=reloadmbed)

    # Toggle
    @commands.command(name="toggle", help="Will toggle on and off the given command")
    @commands.is_owner()
    async def toggle(self, ctx:commands.Context, command:str):
        command = self.bot.get_command(command)
        if not command.enabled:
            command.enabled = True
            await ctx.send(F"Enabled {command.name} command")
        else:
            command.enabled = False
            await ctx.send(F"Disabled {command.name} command.")

    # Repeat
    @commands.command(name="repeat", help="Will repeat the given commands the amounts of given time")
    @commands.is_owner()
    async def repeat(self, ctx:commands.Context, time:int, command:str):
        for _ in range(1, time+1):
            await self.bot.process_commands(command)
        await ctx.send(F"Successfully repeated `{command}` - `{time}` times")

    # Shutdown
    @commands.command(name="shutdown",  help="Will shutdown the bot")
    @commands.is_owner()
    async def logout(self, ctx:commands.Context):
        shutdownmbed = discord.Embed(
            color=self.bot.color,
            title="I'm shutting-down",
            timestamp=ctx.message.created_at
        )
        shutdownmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=shutdownmbed)
        await self.bot.close()

    # Blacklist
    @commands.command(name="blacklist", help="Will put the given user to blacklist")
    @commands.is_owner()
    async def blacklist(self, ctx:commands.Context, user:discord.User=None, *, reason:str=None):
        if not reason: reason = "No reason was provided"
        if not user:
            reloadmbed = discord.Embed(
                color=self.bot.color,
                description="",
                timestamp=ctx.message.created_at
            )
            reloadmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
            blacklisted = await self.bot.postgres.fetch("SELECT * FROM blacklist")
            if not blacklisted:
                reloadmbed.title += "Nobody is in Blacklist"
            else:
                reloadmbed.title = "Users in Blacklist"
                for users in blacklisted:
                    user = self.bot.get_user(users["user_id"])
                    reloadmbed.description += F"{user} | {user.mention} - {users['reason']}\n"
            return await ctx.send(embed=reloadmbed)
        blacklisted = await self.bot.postgres.fetchval("SELECT user_id FROM blacklist WHERE user_id=$1", user.id)
        blacklistmbed = discord.Embed(
            color=self.bot.color,
            timestamp=ctx.message.created_at
        )
        blacklistmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        if not blacklisted:
            await self.bot.postgres.execute("INSERT INTO blacklist(user_name,user_id,reason) VALUES($1,$2,$3)", user.name, user.id, reason)
            blacklistmbed.title = F"Added {user} to blacklist"
        else:
            await self.bot.postgres.execute("DELETE FROM blacklist WHERE user_id=$1", user.id)
            blacklistmbed.title = F"Removed {user} from blacklist"
        await ctx.send(embed=blacklistmbed)

    # Screenshot
    @commands.command(name="screenshot", aliases=["ss"], help="Will give a preview from the given website")
    @commands.is_owner()
    @commands.bot_has_guild_permissions(attach_files=True)
    async def screenshot(self, ctx:commands.Context, *, website:str):
        session = await self.bot.session.get(F"https://api.screenshotmachine.com?key=a95edd&url={website}&dimension=1024x768")
        response = io.BytesIO(await session.read())
        session.close()
        ssmbed = discord.Embed(
            color=self.bot.color,
            title="Here is your screenshot",
            timestamp=ctx.message.created_at
        )
        ssmbed.set_image(url="attachment://screenshot.png")
        ssmbed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(file=discord.File(fp=response, filename="screenshot.png"), embed=ssmbed)

    # Template
    @commands.command(name="template", aliases=["te"], help="Will give the guild's template")
    @commands.is_owner()
    @commands.guild_only()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.bot_has_guild_permissions(manage_guild=True)
    async def template(self, ctx:commands.Context):
        tembed = discord.Embed(
            color=self.bot.color,
            title="Please check your DM",
            timestamp=ctx.message.created_at
        )
        tembed.set_footer(text=ctx.author, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=tembed)
        temp = await ctx.guild.templates()
        await ctx.author.send(temp)

def setup(bot):
    bot.add_cog(Owner(bot))