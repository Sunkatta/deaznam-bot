import os
from discord.ext import commands


class DeaznamBot(commands.Bot):
    async def setup_hook(self):
        await self.load_extension('cogs.general.general')
        await self.load_extension('cogs.music.music')

        shouldSyncCommands = os.getenv('SHOULD_SYNC_SLASH_COMMANDS', 'False')

        # Since syncing takes some time, it is advisable to sync only in production.
        if shouldSyncCommands == 'True':
            synced = await self.tree.sync()
            print(f"Synced {len(synced)} commands globally.")
