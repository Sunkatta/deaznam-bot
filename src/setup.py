import discord
from deaznam_bot import DeaznamBot
from discord.ext import commands


async def setup() -> commands.Bot:
    intents = discord.Intents.default()
    intents.message_content = True

    bot = DeaznamBot(command_prefix=commands.when_mentioned_or("/"),
                     intents=intents)

    return bot
