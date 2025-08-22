import unittest
from unittest.mock import AsyncMock, MagicMock

from cogs.music.music import Music
from cogs.music.song import Song


class DisconnectTest(unittest.IsolatedAsyncioTestCase):
    async def test_should_successfully_clear_the_queue_and_disconnect_from_the_connected_channel(self):
        # Arrange
        song_title = "Never Gonna Give You Up"
        song_url = "www.rickroll.com"

        mock_interaction = MagicMock()
        mock_interaction.response.send_message = AsyncMock()
        mock_interaction.guild.voice_client = MagicMock()
        mock_interaction.guild.voice_client.disconnect = AsyncMock()

        mock_bot = MagicMock()
        mock_bot.loop = None

        music_cog = Music(mock_bot)
        music_cog.songQueue.put(Song(song_title, song_url, None))

        # Act
        await music_cog.disconnect.callback(music_cog, mock_interaction)

        # Assert
        self.assertEqual(music_cog.songQueue.qsize(), 0)
        mock_interaction.guild.voice_client.stop.assert_called_once()
        mock_interaction.guild.voice_client.disconnect.assert_called_once()
        mock_interaction.response.send_message.assert_called_once_with(
            'Sayonara, losers')

    async def test_should_successfully_clear_the_queue_and_not_disconnect_when_not_connected_to_a_channel(self):
        # Arrange
        song_title = "Never Gonna Give You Up"
        song_url = "www.rickroll.com"

        mock_interaction = MagicMock()
        mock_interaction.response.send_message = AsyncMock()
        mock_interaction.guild.voice_client = None

        mock_bot = MagicMock()
        mock_bot.loop = None

        music_cog = Music(mock_bot)
        music_cog.songQueue.put(Song(song_title, song_url, None))

        # Act
        await music_cog.disconnect.callback(music_cog, mock_interaction)

        # Assert
        self.assertEqual(music_cog.songQueue.qsize(), 0)
        mock_interaction.response.send_message.assert_called_once_with(
            'Sayonara, losers')
