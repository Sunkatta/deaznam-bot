import unittest
from unittest.mock import AsyncMock, MagicMock

from cogs.music.music import Music
from cogs.music.song import Song


class SkipTest(unittest.IsolatedAsyncioTestCase):
    async def test_should_successfully_skip_the_current_song(self):
        # Arrange
        song_title = "Never Gonna Give You Up"
        song_url = "www.rickroll.com"

        mock_interaction = MagicMock()
        mock_interaction.response.send_message = AsyncMock()
        mock_interaction.guild.voice_client = MagicMock()

        mock_bot = MagicMock()
        mock_bot.loop = None

        music_cog = Music(mock_bot)
        music_cog.songQueue.put(Song(song_title, song_url, None))

        # Act
        await music_cog.skip.callback(music_cog, mock_interaction)

        # Assert
        self.assertEqual(music_cog.songQueue.qsize(), 1)
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

        music_cog = Music(mock_bot)

        # Act
        await music_cog.skip.callback(music_cog, mock_interaction)

        # Assert
        self.assertEqual(music_cog.songQueue.qsize(), 0)
        self.assertEqual(
            mock_interaction.guild.voice_client.stop.call_count, 0)
        mock_interaction.response.send_message.assert_called_once_with(
            "Can't skip the void, bozo")
