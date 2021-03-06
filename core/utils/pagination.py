import discord

class Paginator(discord.ui.View):
    def __init__(self, ctx, embeds):
        super().__init__(timeout=5)
        self.ctx = ctx
        self.page = 1
        self.embeds = embeds

    @discord.ui.button(emoji="⏮", style=discord.ButtonStyle.green)
    async def previous(self, button:discord.ui.Button, interaction:discord.Interaction):
        if self.page == 0:
            button.disabled = True
        self.page -= 1
        await interaction.response.edit_message(embed=self.embeds[self.page])

    @discord.ui.button(emoji="⏹", style=discord.ButtonStyle.red)
    async def stop(self, button:discord.ui.Button, interaction:discord.Interaction):
        await interaction.message.delete()

    @discord.ui.button(emoji="⏭", style=discord.ButtonStyle.green)
    async def next(self, button:discord.ui.Button, interaction:discord.Interaction):
        if len(self.embeds) == self.page:
            button.disabled = True
        self.page += 1
        await interaction.response.edit_message(embed=self.embeds[self.page])

    async def on_timeout(self):
        try:
            self.clear_items()
            await self.message.edit(view=self)
        except discord.NotFound:
            return

    async def interaction_check(self, interaction:discord.Interaction):
        if self.page == 0:
            self.previous.disabled = True
        if len(self.embeds) == self.page:
            self.next.disabled = True
        if interaction.user.id == self.ctx.message.author.id:
            return True
        icheckmbed = discord.Embed(
            color=self.ctx.bot.color,
            title="You can't use this",
            description=F"<@{interaction.user.id}> - Only <@{self.ctx.message.author.id}> can use that\nCause they did the command\nIf you wanted to use the command, do what they did",
            timestamp=interaction.message.created_at
        )
        icheckmbed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar.url)
        await interaction.response.send_message(embed=icheckmbed, ephemeral=True)
        return False