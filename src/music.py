import discord
from discord.voice_client import VoiceClient
from discord_slash.model import SlashCommandOptionType
from discord_slash.utils.manage_commands import create_option
from ytdlsource import YTDLSource
from discord.ext import commands
from discord_slash import cog_ext, SlashContext


class Music(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @cog_ext.cog_slash(
        name='join',
        description='Joins the specified channel',
        guild_ids=[261917999064154112]
    )
    async def join(self, ctx: SlashContext, channel: discord.VoiceChannel):
        await ctx.defer()
        voice_client: VoiceClient = ctx.voice_client

        if voice_client is not None:
            return await voice_client.move_to(channel)

        await channel.connect()
        await ctx.send(f'Joined channel: `{channel.name}`')

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
        ],
        guild_ids=[261917999064154112]
    )
    async def play(self, ctx: SlashContext, input: str, channel: discord.VoiceChannel = None):
        await ctx.defer()

        if ctx.voice_client is not None and ctx.voice_client.is_playing():
            # TODO: Implement the queue here
            return await ctx.send('Already playing')
        else:
            player = await YTDLSource.from_url(input, loop=self.bot.loop, stream=True)

        if ctx.author.voice is not None:
            authorChannel = ctx.author.voice.channel
            await authorChannel.connect()

            ctx.voice_client.play(player,
                                  after=lambda e: print('Player error: %s' % e) if e else None)

            await ctx.send(f'Now playing: `{player.title}: {player.url}`')
        elif channel is not None:
            await channel.connect()
            ctx.voice_client.play(player,
                                  after=lambda e: print('Player error: %s' % e) if e else None)

            await ctx.send(f'Now playing: `{player.title}: {player.url}`')
        else:
            await ctx.send('Join a voice channel, dummy')

    @cog_ext.cog_slash(
        name='volume',
        description='Tweak the master volume when in voice channel',
        guild_ids=[261917999064154112]
    )
    async def volume(self, ctx: SlashContext, volume: int):
        voice_client: VoiceClient = ctx.voice_client

        if voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        voice_client.source.volume = volume / 100
        await ctx.send("Changed volume to {}%".format(volume))

    @cog_ext.cog_slash(
        name='stop',
        description='Stop the funk',
        guild_ids=[261917999064154112]
    )
    async def stop(self, ctx: SlashContext):
        voice_client: VoiceClient = ctx.voice_client
        voice_client.stop()
        await ctx.send('Stopped')

    @cog_ext.cog_slash(
        name='resume',
        description='Resume the funk',
        guild_ids=[261917999064154112]
    )
    async def resume(self, ctx: SlashContext):
        voice_client: VoiceClient = ctx.voice_client
        voice_client.resume()
        await ctx.send('Resumed')

    @cog_ext.cog_slash(
        name='pause',
        description='Pause the funk',
        guild_ids=[261917999064154112]
    )
    async def pause(self, ctx: SlashContext):
        voice_client: VoiceClient = ctx.voice_client
        voice_client.pause()
        await ctx.send('Paused')

    @cog_ext.cog_slash(
        name='disconnect',
        description='Disconnect from the current voice channel',
        guild_ids=[261917999064154112]
    )
    async def pause(self, ctx: SlashContext):
        voice_client: VoiceClient = ctx.voice_client
        await voice_client.disconnect()
        await ctx.send('Sayonara, losers')

    # TODO: Figure out how to perform this check with the new library
    # @play.add_check
    # async def ensure_voice(ctx):
    #     if ctx.voice_client is None:
    #         if ctx.author.voice:
    #             await ctx.author.voice.channel.connect()
    #         else:
    #             await ctx.send('You are not connected to a voice channel.')
    #             raise commands.CommandError(
    #                 'Author not connected to a voice channel.')
    #     elif ctx.voice_client.is_playing():
    #         ctx.voice_client.stop()
