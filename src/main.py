#!/usr/bin/env python3

import os
from discord.ext import commands
from setup import setup
from dotenv import load_dotenv

load_dotenv()

bot: commands.Bot = setup()
bot.run(os.getenv('BOT_AUTH_TOKEN'))
