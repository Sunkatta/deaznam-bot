import unittest
from unittest.mock import AsyncMock, MagicMock

from cogs.music.music import Music


class SkipTest(unittest.IsolatedAsyncioTestCase):
    async def test_should_successfully_skip_the_current_song(self):
        # Arrange
        player_id = "1"
        mock_interaction = MagicMock()
        mock_interaction.response.send_message = AsyncMock()
        mock_interaction.guild.voice_client = MagicMock()
        mock_interaction.guild_id = player_id

        mock_bot = MagicMock()
        mock_bot.loop = None

        mock_music_queue = MagicMock()
        mock_music_queue.empty.return_value = False

        mock_music_service = MagicMock()
        mock_music_service.get_song_queue_by_music_player_id = MagicMock()
        mock_music_service.get_song_queue_by_music_player_id.return_value = mock_music_queue

        music_cog = Music(mock_bot, mock_music_service)

        # Act
        await music_cog.skip.callback(music_cog, mock_interaction)

        # Assert
        mock_interaction.guild.voice_client.stop.assert_called_once()
        mock_interaction.response.send_message.assert_called_once_with(
            'Skipped')

    async def test_should_send_a_warning_message_when_queue_is_empty(self):
        # Arrange
        mock_interaction = MagicMock()
        mock_interaction.response.send_message = AsyncMock()
        mock_interaction.guild.voice_client = MagicMock()

        mock_bot = MagicMock()
        mock_bot.loop = None

        mock_music_queue = MagicMock()
        mock_music_queue.empty.return_value = True

        mock_music_service = MagicMock()
        mock_music_service.get_song_queue_by_music_player_id = MagicMock()
        mock_music_service.get_song_queue_by_music_player_id.return_value = mock_music_queue

        music_cog = Music(mock_bot, mock_music_service)

        # Act
        await music_cog.skip.callback(music_cog, mock_interaction)

        # Assert
        self.assertEqual(
            mock_interaction.guild.voice_client.stop.call_count, 0)
        mock_interaction.response.send_message.assert_called_once_with(
            "Can't skip the void, bozo")
