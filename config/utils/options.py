import discord, random

class Colour():

    @property
    def invis():
        colour = 0x2F3136 or 0x36393E
        return colour

    @property
    def random():
        colours = [
            discord.Colour.blue(),
            discord.Colour.blurple(),
            discord.Colour.brand_green(),
            discord.Colour.brand_red(),
            discord.Colour.dark_blue(),
            discord.Colour.dark_gold(),
            discord.Colour.dark_gray(),
            discord.Colour.dark_green(),
            discord.Colour.dark_grey(),
            discord.Colour.dark_magenta(),
            discord.Colour.dark_orange(),
            discord.Colour.dark_purple(),
            discord.Colour.dark_red(),
            discord.Colour.dark_teal(),
            discord.Colour.dark_theme(),
            discord.Colour.darker_gray(),
            discord.Colour.darker_grey(),
            discord.Colour.default(),
            discord.Colour.fuchsia(),
            discord.Colour.gold(),
            discord.Colour.green(),
            discord.Colour.greyple(),
            discord.Colour.light_gray(),
            discord.Colour.light_grey(),
            discord.Colour.lighter_gray(),
            discord.Colour.lighter_grey(),
            discord.Colour.magenta(),
            discord.Colour.og_blurple(),
            discord.Colour.orange(),
            discord.Colour.purple(),
            discord.Colour.random(),
            discord.Colour.red(),
            discord.Colour.teal(),
            discord.Colour.yellow()
        ]
        colour = random.choice(colours)
        return colour