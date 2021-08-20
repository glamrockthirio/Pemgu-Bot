import discord
from discord.ext import commands
import os
import asyncpg
from config.utils.json import read_json, write_json

# def get_prefix_json(bot, message):
#     data = read_json("prefixes")
#     if message.guild:
#         if not str(message.guild.id) in data:
#             return "~b"
#         elif str(message.guild.id) in data:
#             return data[str(message.guild.id)]
#     else:
#         return ""

async def get_prefix_postgresql(bot, message):
    if not message.guild:
        return commands.when_mentioned_or("~b")(bot, message)
    prefix = await bot.db.fetch("SELECT prefix FROM prefixes WHERE guild_id = $1", message.guild.id)
    if len(prefix) == 0:
        await bot.db.execute("INSERT INTO prefixes(guild_id, prefix) VALUES ($1, $2)", message.guild.id, "~b")
    else:
        prefix = prefix[0].get("prefix")
    return commands.when_mentioned_or(prefix)(bot, message)

bot = commands.Bot(command_prefix=get_prefix_postgresql, strip_after_prefix=True, case_insensitive=True, owner_ids={798928603201929306, 494496285676535811}, intents=discord.Intents.all(), status=discord.Status.online, activity=discord.Game(name="@Brevity for prefix | ~b help for help | Made by lvlahraam"))

async def create_db_pool():
    bot.db = await asyncpg.create_pool(database=os.getenv("PDB"), user=os.getenv("PUN"), password=os.getenv("PPW"))
    print("Connection to Postgres was successful")
    await bot.db.execute("CREATE TABLE prefixes (guild_id bigint, prefix text)")
    print("Making a table was successful")

bot.blacklisted = []

@bot.check
async def blacklisted(ctx):
    if ctx.author.id in bot.blacklisted:
        return False
    return True 

for file in sorted(os.listdir("./config/core/")):
    if file.endswith(".py"):
        bot.load_extension(F"config.core.{file[:-3]}")

bot.load_extension('jishaku')
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True" 

bot.loop.run_until_complete(create_db_pool())
bot.run(os.getenv("TOKEN"))
