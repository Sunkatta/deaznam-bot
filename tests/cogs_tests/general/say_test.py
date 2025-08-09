import unittest
from unittest.mock import AsyncMock, MagicMock
from cogs.general.general import General


class SayTest(unittest.IsolatedAsyncioTestCase):
    async def test_should_repeat_the_phrase(self):
        # Arrange
        input = "Hello World!"
        mock_interaction = MagicMock()
        mock_interaction.response.send_message = AsyncMock()
        mock_bot = MagicMock()
        mock_bot.loop = None

        general_cog = General(mock_bot)

        # Act
        await general_cog.say.callback(general_cog, mock_interaction, input)

        # Assert
        mock_interaction.response.send_message.assert_called_once_with(input)

    async def test_should_send_default_message_when_interaction_send_message_throws_exception(self):
        # Arrange
        input = "Hello World!"
        mock_interaction = MagicMock()
        mock_interaction.response.send_message = AsyncMock(
            side_effect=[Exception("fail"), None])
        mock_bot = MagicMock()
        mock_bot.loop = None

        general_cog = General(mock_bot)

        # Act
        await general_cog.say.callback(general_cog, mock_interaction, input)

        # Assert
        self.assertEqual(mock_interaction.response.send_message.call_count, 2)

        with self.assertRaises(Exception):
            mock_interaction.side_effect[0]

        mock_interaction.response.send_message.assert_called_with(
            'My creators are dumbasses and did not teach me how to repeat this...'
        )
