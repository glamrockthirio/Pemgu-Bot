import discord
from discord.ext import commands

class OnMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message:discord.Message):
        if message.author.bot: return
        if message.content in (F"<@{self.bot.user.id}>", F"<@!{self.bot.user.id}>"):
            prefix = await self.bot.postgres.fetchval("SELECT prefix FROM prefixes WHERE guild_id=$1", message.guild.id)
            pfmbed = discord.Embed(
                colour=self.bot.colour,
                title=F"My Prefix here is:",
                description=F"> {self.bot.prefix if not prefix else prefix}",
                timestamp=message.created_at
            )
            pfmbed.set_footer(text=message.author, icon_url=message.author.display_avatar.url)
            await message.channel.send(embed=pfmbed)

    @commands.Cog.listener()
    async def on_message_delete(self, message:discord.Message):
        dmsgmbed = discord.Embed(
            colour=self.bot.colour,
            description=F"**{message.content}** - {message.channel.mention}\n{discord.utils.format_dt(discord.utils.utcnow(), style='F')} ({discord.utils.format_dt(discord.utils.utcnow(), style='R')})"
        )
        dmsgmbed.set_author(name=F"{message.author} - {message.author.id}", icon_url=message.author.display_avatar.url)
        self.bot.dmsgs.append(dmsgmbed)

    @commands.Cog.listener()
    async def on_message_edit(self, before:discord.Message, after:discord.Message):
        self.bot.emsgs.append()
        emsgmbed = discord.Embed(
            colour=self.bot.colour,
            description=F"***Before:***\n**{before.content}**\n{discord.utils.format_dt(discord.utils.utcnow(), style='F')} ({discord.utils.format_dt(discord.utils.utcnow(), style='R')})\n\n***After:***\n{after.content}**\n{discord.utils.format_dt(discord.utils.utcnow(), style='F')} ({discord.utils.format_dt(discord.utils.utcnow(), style='R')})"
        )
        emsgmbed.set_author(name=F"{before.author} - {before.author.id}", icon_url=before.author.display_avatar.url)
        self.bot.emsgs.append(emsgmbed)

def setup(bot):
    bot.add_cog(OnMessage(bot))