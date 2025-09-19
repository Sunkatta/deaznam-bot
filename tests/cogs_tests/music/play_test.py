from queue import Queue
import unittest
from unittest.mock import AsyncMock, MagicMock

from cogs.music.music import Music
from models.song import Song


class PlayTest(unittest.IsolatedAsyncioTestCase):
    async def test_should_successfully_play_a_single_song_when_joined_in_a_channel_and_voice_client_is_not_playing_and_queue_is_empty(self):
        # Arrange
        player_id = "1"
        input = "rick roll"
        song_title = "Never Gonna Give You Up"
        song_url = "www.rickroll.com"

        mock_interaction = MagicMock()
        mock_interaction.response.defer = AsyncMock()
        mock_interaction.response.send_message = AsyncMock()
        mock_interaction.guild_id = player_id
        mock_interaction.guild.voice_client = MagicMock()
        mock_interaction.guild.voice_client.is_playing.return_value = False
        mock_interaction.followup.send = AsyncMock()

        mock_bot = MagicMock()
        mock_bot.loop = AsyncMock()

        mock_music_queue = MagicMock()
        mock_music_queue.empty.return_value = False

        mock_music_service = MagicMock()
        mock_music_service.play = AsyncMock()
        mock_music_service.play.return_value = (
            Queue(), [Song(song_title, song_url, song_url)])
        mock_music_service.get_song_queue_by_music_player_id = MagicMock()
        mock_music_service.get_song_queue_by_music_player_id.return_value = mock_music_queue
        mock_music_service.get_next_song = MagicMock()

        music_cog = Music(mock_bot, mock_music_service)

        # Act
        await music_cog.play.callback(music_cog, mock_interaction, input)

        # Assert
        self.assertTrue(
            any("Now playing" in args[0] for args,
                _ in mock_interaction.followup.send.call_args_list)
        )

    async def test_should_successfully_queue_songs_when_joined_in_a_channel_and_voice_client_is_not_playing(self):
        # Arrange
        input = "rick roll and take on me playlist"
        first_song_title = "Never Gonna Give You Up"
        first_song_url = "www.rickroll.com"
        second_song_title = "Take On Me"
        second_song_url = "www.a-ha-take-on-me.com"

        mock_interaction = MagicMock()
        mock_interaction.response.defer = AsyncMock()
        mock_interaction.response.send_message = AsyncMock()
        mock_interaction.guild.voice_client = MagicMock()
        mock_interaction.guild.voice_client.is_playing.return_value = False
        mock_interaction.followup.send = AsyncMock()

        mock_bot = MagicMock()
        mock_bot.loop = AsyncMock()

        mock_music_queue = MagicMock()
        mock_music_queue.empty.return_value = False

        song_queue = MagicMock()
        song_queue.qsize.return_value = 2

        mock_music_service = MagicMock()
        mock_music_service.play = AsyncMock()
        mock_music_service.play.return_value = (
            song_queue,
            [
                Song(first_song_title, first_song_url, first_song_url),
                Song(second_song_title, second_song_url, second_song_url)
            ])
        mock_music_service.get_song_queue_by_music_player_id = MagicMock()
        mock_music_service.get_song_queue_by_music_player_id.return_value = mock_music_queue
        mock_music_service.get_next_song = MagicMock()

        music_cog = Music(mock_bot, mock_music_service)

        # Act
        await music_cog.play.callback(music_cog, mock_interaction, input)

        # Assert
        self.assertEqual(
            mock_interaction.followup.send.call_count, 2)
        mock_interaction.followup.send.assert_any_call(
            'Queued 2 songs')

    async def test_should_successfully_queue_a_song_when_joined_in_a_channel_and_voice_client_is_playing(self):
        # Arrange
        player_id = "1"
        input = "take on me"
        song_title = "Take On Me"
        song_url = "www.a-ha-take-on-me.com"

        mock_interaction = MagicMock()
        mock_interaction.response.defer = AsyncMock()
        mock_interaction.response.send_message = AsyncMock()
        mock_interaction.guild_id = player_id
        mock_interaction.guild.voice_client = MagicMock()
        mock_interaction.guild.voice_client.is_playing.return_value = True
        mock_interaction.followup.send = AsyncMock()

        mock_bot = MagicMock()
        mock_bot.loop = AsyncMock()

        mock_music_queue = MagicMock()
        mock_music_queue.empty.return_value = False

        song_queue = MagicMock()
        song_queue.qsize.return_value = 1

        mock_music_service = MagicMock()
        mock_music_service.play = AsyncMock()
        mock_music_service.play.return_value = (
            song_queue, [Song(song_title, song_url, song_url)])
        mock_music_service.get_song_queue_by_music_player_id = MagicMock()
        mock_music_service.get_song_queue_by_music_player_id.return_value = mock_music_queue
        mock_music_service.get_next_song = MagicMock()

        music_cog = Music(mock_bot, mock_music_service)

        # Act
        await music_cog.play.callback(music_cog, mock_interaction, input)

        # Assert
        self.assertEqual(
            mock_interaction.followup.send.call_count, 1)
        self.assertTrue(
            any("Next up" in args[0] for args,
                _ in mock_interaction.followup.send.call_args_list)
        )

    async def test_should_successfully_queue_songs_when_joined_in_a_channel_and_voice_client_is_playing(self):
        # Arrange
        input = "rick roll and take on me playlist"
        first_song_title = "Never Gonna Give You Up"
        first_song_url = "www.rickroll.com"
        second_song_title = "Take On Me"
        second_song_url = "www.a-ha-take-on-me.com"

        mock_interaction = MagicMock()
        mock_interaction.response.defer = AsyncMock()
        mock_interaction.response.send_message = AsyncMock()
        mock_interaction.guild.voice_client = MagicMock()
        mock_interaction.guild.voice_client.is_playing.return_value = True
        mock_interaction.followup.send = AsyncMock()

        mock_bot = MagicMock()
        mock_bot.loop = AsyncMock()

        mock_music_queue = MagicMock()
        mock_music_queue.empty.return_value = False

        song_queue = MagicMock()
        song_queue.qsize.return_value = 2

        mock_music_service = MagicMock()
        mock_music_service.play = AsyncMock()
        mock_music_service.play.return_value = (
            song_queue,
            [
                Song(first_song_title, first_song_url, first_song_url),
                Song(second_song_title, second_song_url, second_song_url)
            ]
        )
        mock_music_service.get_song_queue_by_music_player_id = MagicMock()
        mock_music_service.get_song_queue_by_music_player_id.return_value = mock_music_queue
        mock_music_service.get_next_song = MagicMock()

        music_cog = Music(mock_bot, mock_music_service)

        # Act
        await music_cog.play.callback(music_cog, mock_interaction, input)

        # Assert
        self.assertEqual(
            mock_interaction.followup.send.call_count, 2)
        mock_interaction.followup.send.assert_any_call(
            'Queued 2 songs')

    async def test_should_not_play_anything_and_send_a_warning_message_when_author_is_not_joined_in_a_channel_and_channel_is_not_provided(self):
        # Arrange
        input = "rick roll"

        mock_interaction = MagicMock()
        mock_interaction.response.defer = AsyncMock()
        mock_interaction.response.send_message = AsyncMock()
        mock_interaction.guild.voice_client = None
        mock_interaction.user.voice = None
        mock_interaction.followup.send = AsyncMock()

        mock_bot = MagicMock()
        mock_bot.loop = AsyncMock()

        mock_music_service = MagicMock()

        music_cog = Music(mock_bot, mock_music_service)

        # Act
        await music_cog.play.callback(music_cog, mock_interaction, input)

        # Assert
        mock_interaction.followup.send.assert_called_once_with(
            'Join a voice channel, dummy')

# TODO: should cover connecting to author channel and specified channel cases
