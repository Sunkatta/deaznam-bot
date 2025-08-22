import unittest
from unittest.mock import AsyncMock, MagicMock

from cogs.music.music import Music
from cogs.music.song import Song


class StopTest(unittest.IsolatedAsyncioTestCase):
    async def test_should_successfully_stop_the_player_and_clear_the_queue(self):
        # Arrange
        first_song_title = "Never Gonna Give You Up"
        first_song_url = "www.rickroll.com"
        second_song_title = "Take On Me"
        second_song_url = "wwww.takeonme.net"

        mock_interaction = MagicMock()
        mock_interaction.response.send_message = AsyncMock()
        mock_interaction.guild.voice_client = MagicMock()

        mock_bot = MagicMock()
        mock_bot.loop = None

        music_cog = Music(mock_bot)
        music_cog.songQueue.put(Song(first_song_title, first_song_url, None))
        music_cog.songQueue.put(Song(second_song_title, second_song_url, None))

        # Act
        await music_cog.stop.callback(music_cog, mock_interaction)

        # Assert
        self.assertEqual(music_cog.songQueue.qsize(), 0)
        mock_interaction.guild.voice_client.stop.assert_called_once()
        mock_interaction.response.send_message.assert_called_once_with(
            'Stopped')

    async def test_should_successfully_clear_the_queue_and_not_stop_the_player_when_not_connected_to_a_channel(self):
        # Arrange
        first_song_title = "Never Gonna Give You Up"
        first_song_url = "www.rickroll.com"
        second_song_title = "Take On Me"
        second_song_url = "wwww.takeonme.net"

        mock_interaction = MagicMock()
        mock_interaction.response.send_message = AsyncMock()
        mock_interaction.guild.voice_client = None

        mock_bot = MagicMock()
        mock_bot.loop = None

        music_cog = Music(mock_bot)
        music_cog.songQueue.put(Song(first_song_title, first_song_url, None))
        music_cog.songQueue.put(Song(second_song_title, second_song_url, None))

        # Act
        await music_cog.stop.callback(music_cog, mock_interaction)

        # Assert
        self.assertEqual(music_cog.songQueue.qsize(), 0)
        mock_interaction.response.send_message.assert_called_once_with(
            'Stopped')
