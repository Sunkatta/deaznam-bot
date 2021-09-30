from os import name
import discord
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
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()
        await ctx.send('Joined')

    @cog_ext.cog_slash(
        name='play',
        description='Time to get funky',
        guild_ids=[261917999064154112]
    )
    async def play(self, ctx: SlashContext, input: str):
        await ctx.defer()
        player = await YTDLSource.from_url(input, stream=True)

        # TODO: Add check if bot is already joined

        channel = ctx.author.voice.channel
        await channel.connect()
        ctx.voice_client.play(player,
                              after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send(f'Now playing: `{player.title}: {player.url}`')

    @cog_ext.cog_slash(
        name='volume',
        description='Tweak the master volume when in voice channel',
        guild_ids=[261917999064154112]
    )
    async def volume(self, ctx, volume: int):
        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send("Changed volume to {}%".format(volume))

    @cog_ext.cog_slash(
        name='stop',
        description='Stop the funk',
        guild_ids=[261917999064154112]
    )
    async def stop(self, ctx: SlashContext):
        await ctx.voice_client.disconnect()
        await ctx.send('Stopped')

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
