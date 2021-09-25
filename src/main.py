import os
from dotenv import load_dotenv
import discord

load_dotenv()
client = discord.Client()


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if (message.author == client.user):
        return

    if (message.content.startswith('/hello')):
        await message.channel.send('Hello!')

client.run(os.getenv('BOT_AUTH_TOKEN'))
