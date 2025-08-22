import unittest
from unittest.mock import AsyncMock, MagicMock

from cogs.music.music import Music
from cogs.music.song import Song


class PlayTest(unittest.IsolatedAsyncioTestCase):
    async def test_should_successfully_play_a_single_song_when_joined_in_a_channel_and_voice_client_is_not_playing_and_queue_is_empty(self):
        # Arrange
        input = "rick roll"

        mock_interaction = MagicMock()
        mock_interaction.response.defer = AsyncMock()
        mock_interaction.response.send_message = AsyncMock()
        mock_interaction.guild.voice_client = MagicMock()
        mock_interaction.guild.voice_client.is_playing.return_value = False
        mock_interaction.followup.send = AsyncMock()

        mock_bot = MagicMock()
        mock_bot.loop = AsyncMock()

        music_cog = Music(mock_bot)

        # Act
        await music_cog.play.callback(music_cog, mock_interaction, input)

        # Assert
        self.assertEqual(music_cog.songQueue.qsize(), 0)
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

        music_cog = Music(mock_bot)

        # TODO: This is a scuffed way. Ideally, we should mock "ytdl.extract_info"
        # and leave the play command to do the job entirely on its own.
        music_cog.songQueue.put(Song(first_song_title, first_song_url, None))
        music_cog.songQueue.put(Song(second_song_title, second_song_url, None))

        # Act
        await music_cog.play.callback(music_cog, mock_interaction, input)

        # Assert
        self.assertEqual(music_cog.songQueue.qsize(), 2)
        self.assertEqual(
            mock_interaction.followup.send.call_count, 2)
        mock_interaction.followup.send.assert_any_call(
            'Queued 1 songs')

    async def test_should_successfully_queue_a_song_when_joined_in_a_channel_and_voice_client_is_playing(self):
        # Arrange
        input = "take on me"

        mock_interaction = MagicMock()
        mock_interaction.response.defer = AsyncMock()
        mock_interaction.response.send_message = AsyncMock()
        mock_interaction.guild.voice_client = MagicMock()
        mock_interaction.guild.voice_client.is_playing.return_value = True
        mock_interaction.followup.send = AsyncMock()

        mock_bot = MagicMock()
        mock_bot.loop = AsyncMock()

        music_cog = Music(mock_bot)

        # Act
        await music_cog.play.callback(music_cog, mock_interaction, input)

        # Assert
        self.assertEqual(music_cog.songQueue.qsize(), 1)
        self.assertEqual(
            mock_interaction.followup.send.call_count, 1)
        self.assertTrue(
            any("Next up" in args[0] for args,
                _ in mock_interaction.followup.send.call_args_list)
        )

    async def test_should_successfully_queue_songs_when_joined_in_a_channel_and_voice_client_is_playing(self):
        # Arrange
        input = "fiki - helicopter"
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

        music_cog = Music(mock_bot)

        # TODO: This is a scuffed way. Ideally, we should mock "ytdl.extract_info"
        # and leave the play command to do the job entirely on its own.
        music_cog.songQueue.put(Song(first_song_title, first_song_url, None))
        music_cog.songQueue.put(Song(second_song_title, second_song_url, None))

        # Act
        await music_cog.play.callback(music_cog, mock_interaction, input)

        # Assert
        self.assertEqual(music_cog.songQueue.qsize(), 3)
        self.assertEqual(
            mock_interaction.followup.send.call_count, 2)
        mock_interaction.followup.send.assert_any_call(
            'Queued 1 songs')

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

        music_cog = Music(mock_bot)

        # Act
        await music_cog.play.callback(music_cog, mock_interaction, input)

        # Assert
        self.assertEqual(music_cog.songQueue.qsize(), 0)
        mock_interaction.followup.send.assert_called_once_with(
            'Join a voice channel, dummy')

# TODO: should cover song suggestion cases as well as connecting to author channel and specified channel
