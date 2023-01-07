#!/usr/bin/env python3

import os
import discord
import asyncio
from discord.ext import commands
from discord.ext.commands import Greedy, Context
from music import Music
from dotenv import load_dotenv
from typing import Literal, Optional

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=commands.when_mentioned_or("/"),
                   intents=intents)


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


@bot.command()
@commands.guild_only()
@commands.is_owner()
async def sync(ctx: Context, guilds: Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
    if not guilds:
        if spec == "~":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()

        await ctx.send(
            f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
        )
        return

    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1

    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")


@bot.tree.command(
    name='say',
    description='Repeat a phrase'
)
async def say(interaction: discord.Interaction, *, input: str):
    await interaction.response.send_message(input)


@say.error
async def say_error(interaction: discord.Interaction, error):
    await interaction.response.send_message('My creators are dumbasses and did not teach me how to repeat this...')


asyncio.run(bot.add_cog(Music(bot)))
bot.run(os.getenv('BOT_AUTH_TOKEN'))
