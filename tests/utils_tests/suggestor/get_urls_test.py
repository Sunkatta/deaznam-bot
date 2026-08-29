import unittest
from unittest.mock import patch

from utils.suggestor import get_urls


class GetUrlsTest(unittest.TestCase):

    def test_returns_urls_from_search_results(self):
        # Arrange
        input_query = "python unittest"
        suggest_query = "python testing"
        limit = 3
        search_results = [
            {"link": "https://www.youtube.com/watch?v=1"},
            {"link": "https://www.youtube.com/watch?v=2"},
            {"link": "https://www.youtube.com/watch?v=3"},
        ]

        with patch("utils.suggestor.__search", return_value=search_results) as mock_search:
            # Act
            result = get_urls(input_query, suggest_query, limit)

        # Assert
        self.assertEqual(
            [
                "https://www.youtube.com/watch?v=1",
                "https://www.youtube.com/watch?v=2",
                "https://www.youtube.com/watch?v=3",
            ],
            result,
        )
        mock_search.assert_called_once_with(input_query, limit)

    def test_searches_suggestion_when_initial_search_returns_no_results(self):
        # Arrange
        input_query = "python unittest"
        suggest_query = "python testing"
        limit = 2
        suggestion_results = [
            {"link": "https://www.youtube.com/watch?v=10"},
            {"link": "https://www.youtube.com/watch?v=20"},
        ]

        with patch(
            "utils.suggestor.__search",
            side_effect=[[], suggestion_results],
        ) as mock_search:
            # Act
            result = get_urls(input_query, suggest_query, limit)

        # Assert
        self.assertEqual(
            [
                "https://www.youtube.com/watch?v=10",
                "https://www.youtube.com/watch?v=20",
            ],
            result,
        )
        self.assertEqual(
            [
                unittest.mock.call(input_query, limit),
                unittest.mock.call(suggest_query, limit),
            ],
            mock_search.call_args_list,
        )

    def test_returns_empty_list_when_both_searches_return_no_results(self):
        # Arrange
        input_query = "query"
        suggest_query = "suggestion"
        limit = 5

        with patch("utils.suggestor.__search", side_effect=[[], []]) as mock_search:
            # Act
            result = get_urls(input_query, suggest_query, limit)

        # Assert
        self.assertEqual([], result)
        self.assertEqual(2, mock_search.call_count)
