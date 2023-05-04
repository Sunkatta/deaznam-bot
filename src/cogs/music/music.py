import discord
import asyncio
import yt_dlp
from discord.voice_client import VoiceClient
from discord.ext import commands
from discord import app_commands
from queue import Queue
from cogs.music.song import Song
from utils import suggested
import traceback

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    # bind to ipv4 since ipv6 addresses cause issues sometimes
    'source_address': '0.0.0.0'
}

ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

ytdl = yt_dlp.YoutubeDL(ytdl_format_options)


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
    async def play(self, interaction: discord.Interaction, input: str, channel: discord.VoiceChannel = None, limit: int = None):
        try:
            await interaction.response.defer()

            if interaction.guild.voice_client is None:
                if interaction.user.voice is not None:
                    authorChannel = interaction.user.voice.channel
                    await authorChannel.connect()
                elif channel is not None:
                    await channel.connect()
                else:
                    await interaction.response.send_message('Join a voice channel, dummy')
                    return

            loop = self.bot.loop or asyncio.get_event_loop()

            songsToEnqueue = []
            if 'https://' not in input: # by text
                if '>' in input:
                    parts = input.split('>')
                    input = parts[0]
                    limit = int(parts[1])
                urls = suggested.get(input, limit)
                if not urls:
                    data = await loop.run_in_executor(None, lambda: ytdl.extract_info(input, download=False))
                    if 'entries' in data: # by playlist
                        for entry in data['entries']:
                            song = Song(entry['title'],
                                        entry['webpage_url'],
                                        discord.FFmpegPCMAudio(entry['url'], **ffmpeg_options))

                            songsToEnqueue.append(song)
                    else: # by video url
                        song = Song(data['title'],
                                    data['webpage_url'],
                                    discord.FFmpegPCMAudio(data['url'], **ffmpeg_options))

                        songsToEnqueue.append(song)
                for url in urls:
                    data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
                    song = Song(data['title'],
                                data['webpage_url'],
                                discord.FFmpegPCMAudio(data['url'], **ffmpeg_options))

                    songsToEnqueue.append(song)
            else:
                data = await loop.run_in_executor(None, lambda: ytdl.extract_info(input, download=False))
                if 'entries' in data: # by playlist
                    for entry in data['entries']:
                        song = Song(entry['title'],
                                    entry['webpage_url'],
                                    discord.FFmpegPCMAudio(entry['url'], **ffmpeg_options))

                        songsToEnqueue.append(song)
                else: # by video url
                    song = Song(data['title'],
                                data['webpage_url'],
                                discord.FFmpegPCMAudio(data['url'], **ffmpeg_options))

                    songsToEnqueue.append(song)

            list(map(self.songQueue.put, songsToEnqueue))

            if not interaction.guild.voice_client.is_playing():
                self.play_song(interaction)

                if self.songQueue.qsize() == 0:
                    await interaction.followup.send(f'Now playing: `{self.currentSong.title} - {self.currentSong.webpage_url}`')
                else:
                    await interaction.followup.send(f'Queued {str(len(songsToEnqueue))} songs')
            elif self.songQueue.qsize() == 1 and len(songsToEnqueue) == 1:
                await interaction.followup.send(f'Next up: `{songsToEnqueue[0].title} - {songsToEnqueue[0].webpage_url}`')
            else:
                await interaction.followup.send(f'Queued {str(len(songsToEnqueue))} songs')
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
            return await interaction.response.send_message('Not connected to a voice channel')

        voice_client.source.volume = volume / 100
        await interaction.response.send_message(f'Changed volume to {volume}%')

    @app_commands.command(
        name='stop',
        description='Stop the funk'
    )
    async def stop(self, interaction: discord.Interaction):
        voice_client: VoiceClient = interaction.guild.voice_client
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
        voice_client: VoiceClient = interaction.guild.voice_client
        voice_client.stop()
        self.songQueue.queue.clear()
        await voice_client.disconnect()
        await interaction.response.send_message('Sayonara, losers')

    @app_commands.command(
        name='seppuku',
        description='Seppuku the funk'
    )
    async def seppuku(self, interaction: discord.Interaction):
        await self.disconnect(interaction)
        raise SystemExit

    @app_commands.command(
        name='queue',
        description='Display all upcoming songs'
    )
    async def queue(self, interaction: discord.Interaction):
        message = '`'

        if self.songQueue.empty():
            return await interaction.response.send_message('Queue is empty')
        else:
            message += f'1.{self.currentSong.title}\n'
            i = 0
            for item in self.songQueue.queue:
                message += f'{i + 2}.{item.title}\n'
                i += 1

            message += '`'

            # todo: message can be split if more than 2000 characters
            try:
                return await interaction.response.send_message(message)
            except:
                print(traceback.format_exc())
                return await interaction.response.send_message('Queue ooopsy')

    def play_song(self, interaction: discord.Interaction):
        if not self.songQueue.empty():
            self.currentSong: Song = self.songQueue.get()
            interaction.guild.voice_client.play(self.currentSong.player,
                                                after=lambda e: self.play_song(interaction))
