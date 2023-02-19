import discord
import asyncio
from cogs.music.music import Music
from cogs.general.general import General
from discord.ext import commands


def setup() -> commands.Bot:
    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix=commands.when_mentioned_or("/"),
                       intents=intents)

    asyncio.run(bot.add_cog(General(bot)))
    asyncio.run(bot.add_cog(Music(bot)))

    return bot
