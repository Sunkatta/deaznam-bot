import unittest

from utils.suggestor import get_suggestions


class GetSuggestionsTest(unittest.TestCase):

    def test_returns_matching_tag_when_title_word_and_tag_match(self):
        # Arrange
        title_words = ["Best", "Python", "Tutorial"]
        tags = ["programming", "python", "tutorial"]

        # Act
        result = get_suggestions(title_words, tags)

        # Assert
        self.assertEqual("python", result)

    def test_matching_is_case_insensitive(self):
        # Arrange
        title_words = ["Python"]
        tags = ["PYTHON"]

        # Act
        result = get_suggestions(title_words, tags)

        # Assert
        self.assertEqual("python", result)

    def test_returns_tag_when_tag_is_contained_in_title_word(self):
        # Arrange
        title_words = ["programming"]
        tags = ["gram"]

        # Act
        result = get_suggestions(title_words, tags)

        # Assert
        self.assertEqual("gram", result)

    def test_returns_first_tag_when_no_title_word_matches(self):
        # Arrange
        title_words = ["cooking", "recipe"]
        tags = ["python", "programming"]

        # Act
        result = get_suggestions(title_words, tags)

        # Assert
        self.assertEqual("python", result)

    def test_returns_first_two_title_words_when_tags_are_empty(self):
        # Arrange
        title_words = ["learn", "python", "quickly"]
        tags = []

        # Act
        result = get_suggestions(title_words, tags)

        # Assert
        self.assertEqual("learn python", result)

    def test_returns_all_title_words_when_fewer_than_two_exist(self):
        # Arrange
        title_words = ["python"]
        tags = []

        # Act
        result = get_suggestions(title_words, tags)

        # Assert
        self.assertEqual("python", result)
