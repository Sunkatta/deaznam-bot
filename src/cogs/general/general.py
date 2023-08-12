import discord
import asyncio
from discord.ext import commands
from discord.ext.commands import Greedy, Context
from typing import Literal, Optional
from discord import app_commands


class General(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'We have logged in as {self.bot.user}')
        await self.bot.change_presence(activity=discord.Game(name="with myself"))

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        # Ignore if change from voice channels not from bot
        if not member.id == self.bot.user.id:
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
                    print(f'Disconnected due to inactivity from Server: {after.channel.guild.name if after.channel.guild else "No Guild"}, Channel: {after.channel.name}')

                    break

    # TODO: fix
    @app_commands.command()
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

    @app_commands.command(
        name='say',
        description='Repeat a phrase'
    )
    async def say(self, interaction: discord.Interaction, input: str):
        try:
            await interaction.response.send_message(input)
        except:
            await interaction.response.send_message('My creators are dumbasses and did not teach me how to repeat this...')
