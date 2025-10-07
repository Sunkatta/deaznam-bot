import asyncio
from queue import Queue
import discord
from discord.voice_client import VoiceClient
from discord.ext import commands
from discord import app_commands
from models.song import Song
from services.music_service import MusicService
from utils import discord_message
from utils.config import ffmpeg_options
import traceback


class Music(commands.Cog):
    def __init__(self, bot: commands.Bot, music_service: MusicService) -> None:
        self.bot = bot
        self.currentSong: Song = None
        self.music_service = music_service
        self.idle_tasks: dict[str, asyncio.Task] = {}

    @app_commands.command(
        name='join',
        description='Joins the specified channel'
    )
    async def join(self, interaction: discord.Interaction, channel: discord.VoiceChannel):
        try:
            await interaction.response.defer()
            voice_client: VoiceClient = interaction.guild.voice_client

            if voice_client is not None:
                return await voice_client.move_to(channel)

            await channel.connect()
            self.music_service.add_music_player(str(interaction.guild_id))
            await self.__send_message(
                interaction, f'Joined channel: `{channel.name}`')
        except:
            print(traceback.format_exc())
            await interaction.response.send_message('I did an whoopsie... Please try that again...')

    @app_commands.command(
        name='play',
        description='Time to get funky',
    )
    async def play(self, interaction: discord.Interaction, input: str, channel: discord.VoiceChannel = None, limit: int = 1):
        try:
            await interaction.response.defer()

            if interaction.guild.voice_client is None:
                if interaction.user.voice is not None:
                    authorChannel = interaction.user.voice.channel
                    await authorChannel.connect()
                elif channel is not None:
                    await channel.connect()
                else:
                    await self.__send_message(interaction, 'Join a voice channel, dummy')
                    return

            (song_queue, songs_to_enqueue) = await self.music_service.play(str(interaction.guild_id), input, limit)

            if not interaction.guild.voice_client.is_playing():
                self.__play_song(interaction)

                if song_queue.qsize() == 0:
                    await interaction.followup.send(f'Now playing: {discord_message.full_text(self.currentSong)}')
                else:
                    await interaction.followup.send(f'Queued {str(len(songs_to_enqueue))} songs')
                    await self.__display_queue(interaction, songs_to_enqueue)
            elif song_queue.qsize() == 1 and len(songs_to_enqueue) == 1:
                await interaction.followup.send(f'Next up: {discord_message.full_text(songs_to_enqueue[0])}')
            else:
                await interaction.followup.send(f'Queued {str(len(songs_to_enqueue))} songs')
                await self.__display_queue(interaction, songs_to_enqueue)
        except:
            print(traceback.format_exc())
            await interaction.followup.send('I did an whoopsie... Please try that again...')

    @app_commands.command(
        name='volume',
        description='Tweak the master volume when in voice channel'
    )
    async def volume(self, interaction: discord.Interaction, volume: int):
        voice_client: VoiceClient = interaction.guild.voice_client

        if voice_client is None:
            await interaction.response.send_message('Not connected to a voice channel')
            return

        voice_client.source.volume = volume / 100
        await interaction.response.send_message(f'Changed volume to {volume}%')

    @app_commands.command(
        name='stop',
        description='Stop the funk'
    )
    async def stop(self, interaction: discord.Interaction):
        voice_client: VoiceClient = interaction.guild.voice_client
        if voice_client:
            voice_client.stop()
        self.music_service.remove_music_player_by_id(str(interaction.guild_id))
        await interaction.response.send_message('Stopped')

    @app_commands.command(
        name='skip',
        description='Skip the current song'
    )
    async def skip(self, interaction: discord.Interaction):
        queue = self.music_service.get_song_queue_by_music_player_id(
            str(interaction.guild_id))

        if queue is None or queue.empty():
            await interaction.response.send_message("Can't skip the void, bozo")
        else:
            voice_client: VoiceClient = interaction.guild.voice_client
            voice_client.stop()
            await interaction.response.send_message('Skipped')

    @app_commands.command(
        name='resume',
        description='Resume the funk'
    )
    async def resume(self, interaction: discord.Interaction):
        voice_client: VoiceClient = interaction.guild.voice_client
        voice_client.resume()
        await interaction.response.send_message('Resumed')

    @app_commands.command(
        name='pause',
        description='Pause the funk'
    )
    async def pause(self, interaction: discord.Interaction):
        voice_client: VoiceClient = interaction.guild.voice_client
        voice_client.pause()
        await interaction.response.send_message('Paused')

    @app_commands.command(
        name='disconnect',
        description='Disconnect from the current voice channel'
    )
    async def disconnect(self, interaction: discord.Interaction):
        try:
            await interaction.response.defer()

            voice_client: VoiceClient = interaction.guild.voice_client

            if voice_client:
                voice_client.stop()
                await voice_client.disconnect()

            self.music_service.remove_music_player_by_id(
                str(interaction.guild_id))
            await self.__send_message(interaction, 'Sayonara, losers')
        except:
            print(traceback.format_exc())

    @app_commands.command(
        name='queue',
        description='Display all upcoming songs'
    )
    async def queue(self, interaction: discord.Interaction):
        song_queue = self.music_service.get_song_queue_by_music_player_id(
            str(interaction.guild_id))

        await self.__display_queue(interaction, list(song_queue.queue if song_queue is not None else []))

    def cancel_idle_task(self, guild_id: str):
        task = self.idle_tasks.pop(guild_id, None)
        if task:
            task.cancel()

    async def __display_queue(self, interaction: discord.Interaction, queue: list):
        try:
            if not queue:
                await interaction.response.send_message('Queue is empty')
                return

            message = discord_message.formatted(queue, 1)
            if len(message) > discord_message.MAX_MESSAGE_SIZE:
                chunks = discord_message.chunks(queue)
                for chunk_index, chunk in enumerate(chunks):
                    chunk_message = discord_message.formatted(
                        chunk, chunk_index * discord_message.CHUNK_SIZE + 1)
                    await self.__send_message(interaction, chunk_message)
            else:
                await self.__send_message(interaction, message)
        except:
            print(traceback.format_exc())
            await self.__send_message(interaction, 'I did an queueuepsie... Please try that again...')

    def __play_song(self, interaction: discord.Interaction):
        player_id = str(interaction.guild_id)
        song_queue = self.music_service.get_song_queue_by_music_player_id(
            player_id)

        if not song_queue.empty():
            # Cancel any existing idle timer for this guild
            task = self.idle_tasks.pop(player_id, None)
            if task:
                task.cancel()

            self.currentSong: Song = self.music_service.get_next_song(
                player_id)
            interaction.guild.voice_client.play(discord.FFmpegPCMAudio(self.currentSong.url, **ffmpeg_options),
                                                after=lambda e: self.__play_song(interaction))
        else:
            self.__start_idle_timer(interaction.guild, song_queue)

    def __start_idle_timer(self, guild: discord.Guild, song_queue: Queue[Song]):
        player_id = str(guild.id)

        # Cancel existing timer if running
        if player_id in self.idle_tasks:
            self.idle_tasks[player_id].cancel()

        # Store the new task in the dict
        self.idle_tasks[player_id] = self.bot.loop.create_task(
            self.__timer(guild, song_queue, player_id)
        )

    async def __timer(self, guild: discord.Guild, song_queue: Queue[Song], player_id: str):
        await asyncio.sleep(600)
        voice: VoiceClient = guild.voice_client

        if voice and not voice.is_playing() and song_queue.empty():
            await voice.disconnect()
            self.music_service.remove_music_player_by_id(player_id)
            print(f"Disconnected from {guild.name} due to inactivity.")

    async def __send_message(self, interaction: discord.Interaction, message: str):
        if interaction.response.is_done():
            await interaction.followup.send(message)
        else:
            await interaction.response.send_message(message)


async def setup(bot: commands.Bot):
    if not hasattr(bot, "music_service"):
        bot.music_service = MusicService()

    await bot.add_cog(Music(bot, bot.music_service))
