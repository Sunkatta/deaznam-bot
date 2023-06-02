import discord
import asyncio
from discord.voice_client import VoiceClient
from discord.ext import commands
from discord import app_commands
from queue import Queue
from cogs.music.song import Song
from utils import discord_message, suggested
from utils.config import ytdl, ffmpeg_options
import traceback

class Music(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.currentSong: Song = None
        self.songQueue = Queue()

    @app_commands.command(
        name='join',
        description='Joins the specified channel'
    )
    async def join(self, interaction: discord.Interaction, channel: discord.VoiceChannel):
        try:
            voice_client: VoiceClient = interaction.guild.voice_client

            if voice_client is not None:
                return await voice_client.move_to(channel)

            await channel.connect()
            await interaction.response.send_message(f'Joined channel: `{channel.name}`')
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

            loop = self.bot.loop or asyncio.get_event_loop()

            entries_info = await self.__prep_entries(loop, input)
            songs_to_enqueue = entries_info['songs_to_enqueue']

            if limit > 1:
                urls = suggested.urls(input, entries_info['suggest'], limit)
                for url in urls:
                    if entries_info['url'] == url:
                        continue
                    suggest_entries_info = await self.__prep_entries(loop, url)
                    songs_to_enqueue.extend(suggest_entries_info['songs_to_enqueue'])

            list(map(self.songQueue.put, songs_to_enqueue))

            if not interaction.guild.voice_client.is_playing():
                self.__play_song(interaction)

                if self.songQueue.qsize() == 0:
                    await interaction.followup.send(f'Now playing: `{self.currentSong.title} - {self.currentSong.webpage_url}`')
                else:
                    await interaction.followup.send(f'Queued {str(len(songs_to_enqueue))} songs')
                    await self.__queue(interaction, songs_to_enqueue)
            elif self.songQueue.qsize() == 1 and len(songs_to_enqueue) == 1:
                await interaction.followup.send(f'Next up: `{songs_to_enqueue[0].title} - {songs_to_enqueue[0].webpage_url}`')
            else:
                await interaction.followup.send(f'Queued {str(len(songs_to_enqueue))} songs')
                await self.__queue(interaction, songs_to_enqueue)
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
        self.songQueue.queue.clear()
        await interaction.response.send_message('Stopped')

    @app_commands.command(
        name='skip',
        description='Skip the current song'
    )
    async def skip(self, interaction: discord.Interaction):
        if self.songQueue.empty():
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
        await self.__disconnect(interaction)

    async def __disconnect(self, interaction: discord.Interaction, message: str = 'Sayonara'):
        voice_client: VoiceClient = interaction.guild.voice_client
        if voice_client:
            voice_client.stop()
            await voice_client.disconnect()
        self.songQueue.queue.clear()

        try:
            await interaction.response.send_message(f'{message}, losers')
        except:
            print(traceback.format_exc())

    @app_commands.command(
        name='seppuku',
        description='Seppuku the funk'
    )
    async def seppuku(self, interaction: discord.Interaction):
        await self.__disconnect(interaction, 'Seppukunara')
        raise SystemExit

    @app_commands.command(
        name='queue',
        description='Display all upcoming songs'
    )
    async def queue(self, interaction: discord.Interaction):
        await self.__queue(interaction, self.songQueue.queue)

    async def __queue(self, interaction: discord.Interaction, queue: list):
        if not queue:
            await interaction.response.send_message('Queue is empty')
            return

        message = discord_message.formatted(queue, 1)
        try:
            if len(message) > 1990:
                chunks = discord_message.chunks(queue)
                for chunk_index, chunk in enumerate(chunks):
                    chunk_message = discord_message.formatted(chunk, chunk_index * 15 + 1)
                    await self.__send_message(interaction, chunk_message)
            else:
                await self.__send_message(interaction, message)
        except:
            print(traceback.format_exc())
            await interaction.response.send_message('I did an queueuepsie... Please try that again...')

    def __play_song(self, interaction: discord.Interaction):
        if not self.songQueue.empty():
            self.currentSong: Song = self.songQueue.get()
            interaction.guild.voice_client.play(self.currentSong.player,
                                                after=lambda e: self.__play_song(interaction))

    async def __prep_entries(self, loop: asyncio.AbstractEventLoop, input: str) -> list:
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(input, download=False))
        songs_to_enqueue = []
        if 'entries' in data:
            for entry in data['entries']:
                prep_entry = self.__prep_entry(entry)
                songs_to_enqueue.append(prep_entry['song'])
        else:
            prep_entry = self.__prep_entry(data)
            songs_to_enqueue.append(prep_entry['song'])
        songs = {'songs_to_enqueue': songs_to_enqueue}
        return {**songs, **prep_entry['latest_info']}

    def __prep_entry(self, entry: dict) -> dict:
        song = Song(entry['title'],
                    entry['webpage_url'],
                    discord.FFmpegPCMAudio(entry['url'], **ffmpeg_options))

        suggest = suggested.spicy_take(entry['title'].split(' '), entry['tags'])
        return {
            'song': song,
            'latest_info': {
                'url': entry['webpage_url'],
                'suggest': suggest
            }
        }

    async def __send_message(self, interaction: discord.Interaction, message: str):
        if interaction.response.is_done():
            await interaction.followup.send(message)
        else: # from queue command
            await interaction.response.send_message(message)