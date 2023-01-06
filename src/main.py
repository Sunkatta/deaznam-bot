#!/usr/bin/env python3

import os
import discord
import asyncio
from discord.ext import commands
from discord_slash import SlashCommand
from music import Music
from dotenv import load_dotenv

load_dotenv()

bot = commands.Bot(command_prefix=commands.when_mentioned_or("/"))
slash = SlashCommand(bot, sync_commands=True)


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    await bot.change_presence(activity=discord.Game(name="with myself"))


@bot.event
async def on_voice_state_update(member, before, after):
    # Ignore if change from voice channels not from bot
    if not member.id == bot.user.id:
        return
    # Ignore if change from voice channels was triggered by disconnect()
    elif before.channel is not None:
        return
    else:
        voice = after.channel.guild.voice_client

        while True:
            await asyncio.sleep(600)

            if voice.is_playing() == False:
                await voice.disconnect()
                print(
                    f'Disconnected due to inactivity from Server: {after.channel.guild.name}, Channel: {after.channel.name}')
                break


@slash.slash(
    name='say',
    description='Repeat a phrase'
)
async def say(ctx, *, input):
    await ctx.send(input)


@say.error
async def say_error(ctx, error):
    await ctx.send('My creators are dumbasses and did not teach me how to repeat this...')


bot.add_cog(Music(bot))
bot.run(os.getenv('BOT_AUTH_TOKEN'))
