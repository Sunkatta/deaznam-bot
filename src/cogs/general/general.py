import discord
from discord.ext import commands
from discord import Member, VoiceClient, VoiceState, app_commands
from cogs.music.music import Music
from services.music_service import MusicService


class General(commands.Cog):
    def __init__(self, bot: commands.Bot, music_service: MusicService) -> None:
        super().__init__()
        self.bot = bot
        self.music_service = music_service
        self.music_cog: Music = None

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'We have logged in as {self.bot.user}')
        await self.bot.change_presence(activity=discord.Game(name="with myself"))

        # Injecting the cog directly since this is the simplest way for now.
        # When more cogs are introduced, we can look into event dispatching via the bot.
        if self.music_cog is None:
            self.music_cog = self.bot.get_cog("Music")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: Member, before: VoiceState, after: VoiceState):
        # Ignore if change from voice channels not from bot
        if member.id != self.bot.user.id:
            return
        # Clear the song queue for the server on disconnect
        elif before.channel is not None and after.channel is None:
            self.music_service.remove_music_player_by_id(
                str(before.channel.guild.id))
            voice: VoiceClient = before.channel.guild.voice_client
            voice.stop()
            self.music_cog.cancel_idle_task(str(before.channel.guild.id))
            return

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
    if not hasattr(bot, "music_service"):
        bot.music_service = MusicService()

    await bot.add_cog(General(bot, bot.music_service))
