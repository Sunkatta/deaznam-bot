import unittest
from unittest.mock import AsyncMock, MagicMock

from cogs.music.music import Music
from models.song import Song
from services.music_service import MusicService


class SkipTest(unittest.IsolatedAsyncioTestCase):
    async def test_should_successfully_skip_the_current_song(self):
        # Arrange
        player_id = "1"
        song_title = "Never Gonna Give You Up"
        song_url = "www.rickroll.com"

        mock_interaction = MagicMock()
        mock_interaction.response.send_message = AsyncMock()
        mock_interaction.guild.voice_client = MagicMock()
        mock_interaction.guild_id = player_id

        mock_bot = MagicMock()
        mock_bot.loop = None

        mock_music_service = MusicService()

        music_cog = Music(mock_bot, mock_music_service)
        mock_music_service.add_music_player(player_id)
        music_player = mock_music_service.music_players[player_id]
        music_player.add_song(Song(song_title, song_url, None))

        # Act
        await music_cog.skip.callback(music_cog, mock_interaction)

        # Assert
        self.assertEqual(music_player.song_queue.qsize(), 0)
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

        mock_music_service = MusicService()

        music_cog = Music(mock_bot, mock_music_service)

        # Act
        await music_cog.skip.callback(music_cog, mock_interaction)

        # Assert
        self.assertEqual(len(mock_music_service.music_players), 0)
        self.assertEqual(
            mock_interaction.guild.voice_client.stop.call_count, 0)
        mock_interaction.response.send_message.assert_called_once_with(
            "Can't skip the void, bozo")
