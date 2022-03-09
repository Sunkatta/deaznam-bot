import discord
from discord.voice_client import VoiceClient
from discord_slash.model import SlashCommandOptionType
from discord_slash.utils.manage_commands import create_option
from ytdlsource import YTDLSource
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from queue import Queue


class Music(commands.Cog):
    currentSong = None

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.songQueue = Queue()

    @cog_ext.cog_slash(
        name='join',
        description='Joins the specified channel'
    )
    async def join(self, ctx: SlashContext, channel: discord.VoiceChannel):
        try:
            await ctx.defer()
            voice_client: VoiceClient = ctx.voice_client

            if voice_client is not None:
                return await voice_client.move_to(channel)

            await channel.connect()
            await ctx.send(f'Joined channel: `{channel.name}`')
        except:
            await ctx.send('I did an whoopsie... Please try that again...')

    @cog_ext.cog_slash(
        name='play',
        description='Time to get funky',
        options=[
            create_option(
                name='input',
                description='URL or search term',
                required=True,
                option_type=SlashCommandOptionType.STRING
            ),
            create_option(
                name='channel',
                description='Target channel',
                required=False,
                option_type=SlashCommandOptionType.CHANNEL
            )
        ]
    )
    async def play(self, ctx: SlashContext, input: str, channel: discord.VoiceChannel = None):
        try:
            await ctx.defer()

            if ctx.voice_client is None:
                if ctx.author.voice is not None:
                    authorChannel = ctx.author.voice.channel
                    await authorChannel.connect()
                elif channel is not None:
                    await channel.connect()
                else:
                    await ctx.send('Join a voice channel, dummy')
                    return

            player = await YTDLSource.from_url(input, loop=self.bot.loop, stream=True)
            self.songQueue.put(player)

            if not ctx.voice_client.is_playing():
                self.play_song(ctx)
                await ctx.send(f'Now playing: `{player.title} - {player.url}`')
            else:
                return await ctx.send(f'Next up: `{player.title} - {player.url}`')
        except:
            await ctx.send('I did an whoopsie... Please try that again...')

    @cog_ext.cog_slash(
        name='volume',
        description='Tweak the master volume when in voice channel'
    )
    async def volume(self, ctx: SlashContext, volume: int):
        voice_client: VoiceClient = ctx.voice_client

        if voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        voice_client.source.volume = volume / 100
        await ctx.send(f'Changed volume to {volume}%')

    @cog_ext.cog_slash(
        name='stop',
        description='Stop the funk'
    )
    async def stop(self, ctx: SlashContext):
        voice_client: VoiceClient = ctx.voice_client
        voice_client.stop()
        self.songQueue.queue.clear()
        await ctx.send('Stopped')

    @cog_ext.cog_slash(
        name='skip',
        description='Skip the current song'
    )
    async def skip(self, ctx: SlashContext):
        await ctx.defer()
        voice_client: VoiceClient = ctx.voice_client
        voice_client.stop()
        await ctx.send('Skipped')

    @cog_ext.cog_slash(
        name='resume',
        description='Resume the funk'
    )
    async def resume(self, ctx: SlashContext):
        voice_client: VoiceClient = ctx.voice_client
        voice_client.resume()
        await ctx.send('Resumed')

    @cog_ext.cog_slash(
        name='pause',
        description='Pause the funk'
    )
    async def pause(self, ctx: SlashContext):
        voice_client: VoiceClient = ctx.voice_client
        voice_client.pause()
        await ctx.send('Paused')

    @cog_ext.cog_slash(
        name='disconnect',
        description='Disconnect from the current voice channel'
    )
    async def disconnect(self, ctx: SlashContext):
        voice_client: VoiceClient = ctx.voice_client
        await voice_client.disconnect()
        await ctx.send('Sayonara, losers')

    @cog_ext.cog_slash(
        name='queue',
        description='Display all upcoming songs'
    )
    async def queue(self, ctx: SlashContext):
        await ctx.defer()
        message = '`'
        i = 1

        if self.songQueue.empty():
            return await ctx.send('Queue is empty')
        else:
            for item in self.songQueue.queue:
                message += f'{i}. {item.title} - {item.url}\n'
                i += 1

            message += '`'
            return await ctx.send(message)

    @cog_ext.cog_slash(
        name='repeat',
        description='Repeat the funk',
        options=[
            create_option(
                name='times',
                description='Number of times to be repeated',
                required=False,
                option_type=SlashCommandOptionType.INTEGER
            )
        ]
    )
    async def repeat(self, ctx: SlashContext, times=0):
        await ctx.defer()
        if times == 0:
            player = await YTDLSource.from_url(self.currentSong.title, loop=self.bot.loop, stream=True)
            self.songQueue.put(player)
            await ctx.send(f'Repeating `{self.currentSong.title} - {self.currentSong.url}`')
        else:
            for x in range(times):
                player = await YTDLSource.from_url(self.currentSong.title, loop=self.bot.loop, stream=True)
                self.songQueue.put(player)

            await ctx.send(f'Repeating {times} times: `{self.currentSong.title} - {self.currentSong.url}`')

    def play_song(self, ctx: SlashContext):
        if not self.songQueue.empty():
            self.currentSong = self.songQueue.get()
            ctx.voice_client.play(self.currentSong,
                                  after=lambda e: self.play_song(ctx))
