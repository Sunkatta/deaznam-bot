import unittest
from unittest.mock import AsyncMock, MagicMock

from cogs.music.music import Music


class VolumeTest(unittest.IsolatedAsyncioTestCase):
    async def test_should_successfully_tweak_the_volume(self):
        # Arrange
        volume = 5

        mock_interaction = MagicMock()
        mock_interaction.response.send_message = AsyncMock()
        mock_interaction.guild.voice_client = MagicMock()

        mock_bot = MagicMock()
        mock_bot.loop = None

        music_cog = Music(mock_bot)

        # Act
        await music_cog.volume.callback(music_cog, mock_interaction, volume)

        # Assert
        expected_volume = 0.05

        self.assertEqual(
            mock_interaction.guild.voice_client.source.volume, expected_volume)
        mock_interaction.response.send_message.assert_called_once_with(
            f'Changed volume to {volume}%')

    async def test_should_send_message_and_not_tweak_volume_when_not_joined_in_channel(self):
        # Arrange
        volume = 5

        mock_interaction = MagicMock()
        mock_interaction.response.send_message = AsyncMock()
        mock_interaction.guild.voice_client = None

        mock_bot = MagicMock()
        mock_bot.loop = None

        music_cog = Music(mock_bot)

        # Act
        await music_cog.volume.callback(music_cog, mock_interaction, volume)

        # Assert
        mock_interaction.response.send_message.assert_called_once_with(
            'Not connected to a voice channel')
