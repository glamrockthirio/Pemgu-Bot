import discord
from discord.ext import commands
from config.utils.stream import player

class Music(commands.Cog, description="Commands to jam out with"):
    def __init__(self, bot):
        self.bot = bot
    
    # Connect
    @commands.command(name="connect", aliases=["cn"], help="Will connect the bot to your voice channel")
    @commands.guild_only()
    async def connect(self, ctx):
        await ctx.trigger_typing()
        if ctx.author.voice.channel and not ctx.voice_client.is_connected():
            await ctx.author.voice.channel.connect()
            await ctx.send("Connected to the voice")
        elif ctx.voice_client.is_connected():
            await ctx.send("Somebody else is using me")
        elif not ctx.author.voice:
            await ctx.send("You are not joined any voice channel")
    
    # Disconnect
    @commands.command(name="disconnect", aliases=["dc"], help="Will disconnect the bot to your voice channel")
    @commands.guild_only()
    async def disconnect(self, ctx):
        await ctx.trigger_typing()
        if not ctx.voice_client.is_connected():
            await ctx.send("Nobody is using me")
        elif ctx.author.voice.channel != ctx.me.voice.channel:
            await ctx.send("Somebody else is using me")
        elif ctx.author.voice.channel == ctx.me.voice.channel:
            await ctx.voice_client.disconnect()
            await ctx.sene("Disconnecting from the voice channel")
    
    # Play
    @commands.command(name="play", aliases=["p"], help="Will play the music given music in your voice channel", usage="<link>")
    async def play(self, ctx, *, url):
        await ctx.trigger_typing()
        if not ctx.voice_voice.is_connected() and ctx.author.voice.channel:
            await ctx.author.voice.channel.connect()
            await ctx.send("Joined your voice channel")
            player(url)
        elif ctx.author.voice.channel == ctx.me.voice.channel:
            await ctx.voice_client.stop()
            player(url)
        elif ctx.author.voice.channel != ctx.me.voice.channel:
            await ctx.send("Somebody else is using me")
        elif not ctx.author.voice:
            await ctx.send("You are not joined any voice channel")
    
    # Pause
    @commands.command(name="pause", aliases=["pa"], help="Will pause the song")
    @commands.guild_only()
    async def pause(self, ctx):
        await ctx.trigger_typing()
        if not ctx.voice_client.is_connected():
            await ctx.send("Nobody is using me")
        elif ctx.author.voice.channel != ctx.me.voice.channel:
            await ctx.send("Somebody else is using me")
        elif ctx.author.voice.channel == ctx.me.voice.channel and ctx.voice_client.is_playing():
            await ctx.voice_client.pause()
            await ctx.sene("Pausing the song")

    # Resume
    @commands.command(name="resume", aliases=["rs"], help="Will resume the song")
    @commands.guild_only()
    async def resume(self, ctx):
        await ctx.trigger_typing()
        if not ctx.voice_client.is_connected():
            await ctx.send("Nobody is using me")
        elif ctx.author.voice.channel != ctx.me.voice.channel:
            await ctx.send("Somebody else is using me")
        elif ctx.author.voice.channel == ctx.me.voice.channel and ctx.voice_client.is_paused():
            await ctx.voice_client.resume()
            await ctx.sene("Resuming the song")

    # Stop
    @commands.command(name="stop", aliases=["so"], help="Will stop the song")
    @commands.guild_only()
    async def stop(self, ctx):
        await ctx.trigger_typing()
        if not ctx.voice_client.is_connected():
            await ctx.send("Nobody is using me")
        elif ctx.author.voice.channel != ctx.me.voice.channel:
            await ctx.send("Somebody else is using me")
        elif ctx.author.voice.channel == ctx.me.voice.channel and ctx.voice_client.is_playing():
            await ctx.voice_client.stop()
            await ctx.sene("Stoping the song")

def setup(bot):
    bot.add_cog(Music(bot))