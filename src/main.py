#!/usr/bin/env python3

import os
import argparse
import asyncio
from discord.ext import commands
from setup import setup
from dotenv import load_dotenv


async def main(env: str):

    # If no argument is specified, use default env for local development.
    dotenv_file = f".env.{env}" if env is not None else ".env"
    print(f'Using environment file {dotenv_file}')
    load_dotenv(dotenv_file, override=True)

    token = os.getenv('BOT_AUTH_TOKEN')

    bot: commands.Bot = await setup()
    await bot.start(token)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--env')
    args = parser.parse_args()

    asyncio.run(main(args.env))
