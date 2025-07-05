import discord
import asyncio
from discord.ext import commands
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
                    guild_name = after.channel.guild.name if (
                        after.channel and after.channel.guild) else 'No Guild'
                    channel_name = after.channel.name if after.channel else 'No Channel'
                    print(
                        f'Disconnected due to inactivity from Server:{guild_name}, Channel: {channel_name}')

                    break

    @app_commands.command(
        name='say',
        description='Repeat a phrase'
    )
    async def say(self, interaction: discord.Interaction, input: str):
        try:
            await interaction.response.send_message(input)
        except:
            await interaction.response.send_message('My creators are dumbasses and did not teach me how to repeat this...')


async def setup(bot: commands.Bot):
    await bot.add_cog(General(bot))
