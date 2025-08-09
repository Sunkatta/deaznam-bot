import unittest
from unittest.mock import AsyncMock, MagicMock
from cogs.music.music import Music


class JoinTest(unittest.IsolatedAsyncioTestCase):
    async def test_should_successfully_join_channel_when_not_joined_anywhere(self):
        # Arrange
        channel_name = "Cool Channel"

        mock_interaction = MagicMock()
        mock_interaction.guild.voice_client = None
        mock_interaction.response.send_message = AsyncMock()

        mock_bot = MagicMock()
        mock_bot.loop = None

        mock_channel = MagicMock()
        mock_channel.connect = AsyncMock()
        mock_channel.name = channel_name

        music_cog = Music(mock_bot)

        # Act
        await music_cog.join.callback(music_cog, mock_interaction, mock_channel)

        # Assert
        mock_channel.connect.assert_called_once()
        mock_interaction.response.send_message.assert_called_once_with(
            f'Joined channel: `{channel_name}`')

    async def test_should_successfully_move_to_target_channel_when_joined_somewhere_else(self):
        # Arrange
        mock_interaction = MagicMock()
        mock_interaction.guild.voice_client = MagicMock()
        mock_interaction.guild.voice_client.move_to = AsyncMock()

        mock_bot = MagicMock()
        mock_bot.loop = None

        mock_channel = MagicMock()

        music_cog = Music(mock_bot)

        # Act
        await music_cog.join.callback(music_cog, mock_interaction, mock_channel)

        # Assert
        mock_interaction.guild.voice_client.move_to.assert_called_once()
        self.assertEqual(mock_channel.connect.call_count, 0)
        self.assertEqual(mock_interaction.response.send_message.call_count, 0)

    async def test_should_send_default_message_when_connect_throws_exception(self):
        # Arrange
        channel_name = "Cool Channel"

        mock_interaction = MagicMock()
        mock_interaction.guild.voice_client = None
        mock_interaction.response.send_message = AsyncMock()

        mock_bot = MagicMock()
        mock_bot.loop = None

        mock_channel = MagicMock()
        mock_channel.connect = AsyncMock(
            side_effect=Exception("fail"))
        mock_channel.name = channel_name

        music_cog = Music(mock_bot)

        # Act
        await music_cog.join.callback(music_cog, mock_interaction, mock_channel)

        # Assert
        with self.assertRaises(Exception):
            mock_channel.side_effect[0]

        self.assertEqual(mock_interaction.response.send_message.call_count, 1)
        mock_interaction.response.send_message.assert_called_with(
            'I did an whoopsie... Please try that again...'
        )

    async def test_should_send_default_message_when_move_to_throws_exception(self):
        # Arrange
        mock_interaction = MagicMock()
        mock_interaction.guild.voice_client = MagicMock()
        mock_interaction.guild.voice_client.move_to = AsyncMock(
            side_effect=Exception("fail"))
        mock_interaction.response.send_message = AsyncMock()

        mock_bot = MagicMock()
        mock_bot.loop = None

        mock_channel = MagicMock()

        music_cog = Music(mock_bot)

        # Act
        await music_cog.join.callback(music_cog, mock_interaction, mock_channel)

        # Assert
        with self.assertRaises(Exception):
            mock_interaction.side_effect[0]

        self.assertEqual(mock_interaction.response.send_message.call_count, 1)
        mock_interaction.response.send_message.assert_called_with(
            'I did an whoopsie... Please try that again...'
        )

    async def test_should_send_default_message_when_send_message_first_call_throws_exception(self):
        # Arrange
        channel_name = "Cool Channel"

        mock_interaction = MagicMock()
        mock_interaction.guild.voice_client = None
        mock_interaction.response.send_message = AsyncMock(
            side_effect=[Exception("fail"), None])

        mock_bot = MagicMock()
        mock_bot.loop = None

        mock_channel = MagicMock()
        mock_channel.connect = AsyncMock()
        mock_channel.name = channel_name

        music_cog = Music(mock_bot)

        # Act
        await music_cog.join.callback(music_cog, mock_interaction, mock_channel)

        # Assert
        with self.assertRaises(Exception):
            mock_interaction.side_effect[0]

        self.assertEqual(mock_interaction.response.send_message.call_count, 2)
        mock_interaction.response.send_message.assert_called_with(
            'I did an whoopsie... Please try that again...'
        )
