import unittest
from unittest.mock import AsyncMock, MagicMock

from cogs.music.music import Music
from models.song import Song
from services.music_service import MusicService


class DisconnectTest(unittest.IsolatedAsyncioTestCase):
    async def test_should_successfully_clear_the_queue_and_disconnect_from_the_connected_channel(self):
        # Arrange
        player_id = "1"
        song_title = "Never Gonna Give You Up"
        song_url = "www.rickroll.com"

        mock_interaction = MagicMock()
        mock_interaction.guild_id = player_id
        mock_interaction.response.defer = AsyncMock()
        mock_interaction.guild.voice_client = MagicMock()
        mock_interaction.guild.voice_client.disconnect = AsyncMock()
        mock_interaction.followup.send = AsyncMock()

        mock_bot = MagicMock()
        mock_bot.loop = None

        mock_music_service = MusicService()
        mock_music_service.add_music_player(player_id)
        music_player = mock_music_service.music_players[player_id]
        music_player.add_song(Song(song_title, song_url, None))

        music_cog = Music(mock_bot, mock_music_service)

        # Act
        await music_cog.disconnect.callback(music_cog, mock_interaction)

        # Assert
        self.assertEqual(music_player.song_queue.qsize(), 0)
        self.assertEqual(len(mock_music_service.music_players), 0)
        mock_interaction.guild.voice_client.stop.assert_called_once()
        mock_interaction.guild.voice_client.disconnect.assert_called_once()
        mock_interaction.followup.send.assert_called_once_with(
            'Sayonara, losers')

    async def test_should_successfully_clear_the_queue_and_not_disconnect_when_not_connected_to_a_channel(self):
        # Arrange
        player_id = "1"
        song_title = "Never Gonna Give You Up"
        song_url = "www.rickroll.com"

        mock_interaction = MagicMock()
        mock_interaction.guild_id = player_id
        mock_interaction.response.defer = AsyncMock()
        mock_interaction.followup.send = AsyncMock()
        mock_interaction.guild.voice_client = None

        mock_bot = MagicMock()
        mock_bot.loop = None

        mock_music_service = MusicService()
        mock_music_service.add_music_player(player_id)
        music_player = mock_music_service.music_players[player_id]
        music_player.add_song(Song(song_title, song_url, None))

        music_cog = Music(mock_bot, mock_music_service)

        # Act
        await music_cog.disconnect.callback(music_cog, mock_interaction)

        # Assert
        self.assertEqual(music_player.song_queue.qsize(), 0)
        self.assertEqual(len(mock_music_service.music_players), 0)
        mock_interaction.followup.send.assert_called_once_with(
            'Sayonara, losers')
