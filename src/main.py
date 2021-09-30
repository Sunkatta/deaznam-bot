import os
from discord.ext import commands
from discord_slash import SlashCommand
from music import Music
from dotenv import load_dotenv

load_dotenv()


bot = commands.Bot(command_prefix=commands.when_mentioned_or("/"),
                   description="I don't know where this text is gonna be visualised...")
slash = SlashCommand(bot, sync_commands=True)


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@slash.slash(
    name='repeat',
    description='Repeat a phrase',
    guild_ids=[261917999064154112]
)
async def repeat(ctx, *, input):
    await ctx.send(input)


@repeat.error
async def repeat_error(ctx, error):
    await ctx.send('My creators are dumbasses and did not teach me how to repeat this...')

bot.add_cog(Music(bot))
bot.run(os.getenv('BOT_AUTH_TOKEN'))
