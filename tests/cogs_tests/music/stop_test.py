import unittest
from unittest.mock import AsyncMock, MagicMock

from cogs.music.music import Music
from models.song import Song
from services.music_service import MusicService


class StopTest(unittest.IsolatedAsyncioTestCase):
    async def test_should_successfully_stop_the_player_and_clear_the_queue(self):
        # Arrange
        player_id = "1"
        first_song_title = "Never Gonna Give You Up"
        first_song_url = "www.rickroll.com"
        second_song_title = "Take On Me"
        second_song_url = "wwww.takeonme.net"

        mock_interaction = MagicMock()
        mock_interaction.guild_id = player_id
        mock_interaction.response.send_message = AsyncMock()
        mock_interaction.guild.voice_client = MagicMock()

        mock_bot = MagicMock()
        mock_bot.loop = None

        mock_music_service = MusicService()
        mock_music_service.add_music_player(player_id)
        music_player = mock_music_service.music_players[player_id]
        music_player.add_song(
            Song(first_song_title, first_song_url, first_song_url))
        music_player.add_song(
            Song(second_song_title, second_song_url, second_song_url))

        music_cog = Music(mock_bot, mock_music_service)

        # Act
        await music_cog.stop.callback(music_cog, mock_interaction)

        # Assert
        self.assertEqual(music_player.song_queue.qsize(), 0)
        self.assertEqual(len(mock_music_service.music_players), 0)
        mock_interaction.guild.voice_client.stop.assert_called_once()
        mock_interaction.response.send_message.assert_called_once_with(
            'Stopped')

    async def test_should_successfully_clear_the_queue_and_not_stop_the_player_when_not_connected_to_a_channel(self):
        # Arrange
        player_id = "1"
        first_song_title = "Never Gonna Give You Up"
        first_song_url = "www.rickroll.com"
        second_song_title = "Take On Me"
        second_song_url = "wwww.takeonme.net"

        mock_interaction = MagicMock()
        mock_interaction.guild_id = player_id
        mock_interaction.response.send_message = AsyncMock()
        mock_interaction.guild.voice_client = None

        mock_bot = MagicMock()
        mock_bot.loop = None

        mock_music_service = MusicService()
        mock_music_service.add_music_player(player_id)
        music_player = mock_music_service.music_players[player_id]
        music_player.add_song(
            Song(first_song_title, first_song_url, first_song_url))
        music_player.add_song(
            Song(second_song_title, second_song_url, second_song_url))

        music_cog = Music(mock_bot, mock_music_service)

        # Act
        await music_cog.stop.callback(music_cog, mock_interaction)

        # Assert
        self.assertEqual(music_player.song_queue.qsize(), 0)
        self.assertEqual(len(mock_music_service.music_players), 0)
        mock_interaction.response.send_message.assert_called_once_with(
            'Stopped')
