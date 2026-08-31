import unittest

from utils.suggestor import get_suggestions


class GetSuggestionsTest(unittest.TestCase):

    def test_returns_matching_tag(self):
        # Arrange
        test_cases = [
            (
                ["Best", "Python", "Tutorial"],
                ["programming", "python", "tutorial"],
                "python",
            ),
            (
                ["Python"],
                ["PYTHON"],
                "python",
            ),
            (
                ["programming"],
                ["gram"],
                "gram",
            ),
        ]

        for title_words, tags, expected in test_cases:
            with self.subTest(title_words=title_words, tags=tags):
                # Act
                result = get_suggestions(title_words, tags)

                # Assert
                self.assertEqual(expected, result)

    def test_returns_first_tag_when_no_title_word_matches(self):
        # Arrange
        title_words = ["cooking", "recipe"]
        tags = ["python", "programming"]
        expected = "python"

        # Act
        result = get_suggestions(title_words, tags)

        # Assert
        self.assertEqual(expected, result)

    def test_returns_first_two_title_words_when_tags_are_empty(self):
        # Arrange
        test_cases = [
            (
                ["learn", "python", "quickly"],
                "learn python",
            ),
            (
                ["python"],
                "python",
            ),
        ]

        for title_words, expected in test_cases:
            with self.subTest(title_words=title_words):
                # Act
                result = get_suggestions(title_words, [])

                # Assert
                self.assertEqual(expected, result)
