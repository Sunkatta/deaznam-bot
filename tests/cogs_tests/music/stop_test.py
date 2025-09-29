import unittest
from unittest.mock import AsyncMock, MagicMock

from cogs.music.music import Music


class StopTest(unittest.IsolatedAsyncioTestCase):
    async def test_should_successfully_stop_the_player_and_clear_the_queue(self):
        # Arrange
        player_id = "1"

        mock_interaction = MagicMock()
        mock_interaction.guild_id = player_id
        mock_interaction.response.send_message = AsyncMock()
        mock_interaction.guild.voice_client = MagicMock()

        mock_bot = MagicMock()
        mock_bot.loop = None

        mock_music_service = MagicMock()

        music_cog = Music(mock_bot, mock_music_service)

        # Act
        await music_cog.stop.callback(music_cog, mock_interaction)

        # Assert
        mock_music_service.remove_music_player_by_id.assert_called_once()
        mock_interaction.guild.voice_client.stop.assert_called_once()
        mock_interaction.response.send_message.assert_called_once_with(
            'Stopped')

    async def test_should_successfully_clear_the_queue_and_not_stop_the_player_when_not_connected_to_a_channel(self):
        # Arrange
        player_id = "1"

        mock_interaction = MagicMock()
        mock_interaction.guild_id = player_id
        mock_interaction.response.send_message = AsyncMock()
        mock_interaction.guild.voice_client = None

        mock_bot = MagicMock()
        mock_bot.loop = None

        mock_music_service = MagicMock()

        music_cog = Music(mock_bot, mock_music_service)

        # Act
        await music_cog.stop.callback(music_cog, mock_interaction)

        # Assert
        mock_music_service.remove_music_player_by_id.assert_called_once()
        self.assertEqual(len(mock_music_service.music_players), 0)
        mock_interaction.response.send_message.assert_called_once_with(
            'Stopped')
