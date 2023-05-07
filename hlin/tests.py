from unittest.mock import patch , MagicMock
from hlin.utils.quote_utils import get_quote , get_quote_from_db, post_quote
from hlin.settings import API_URL
import pytest 

@pytest.fixture
def full_user():
    """Represents a valid user with full data. """
    return {
        'email': 'full@example.com',
        'name': 'Maximus Plenus',
        'age': 65,
        'role': 'emperor',
    }


class Test_Quotes:
    @patch('hlin.utils.quote_utils.get_quote')
    def test_get_quote(self, mock_get_quote):
        # mock the response of the API
        mock_get_quote.return_value = {
            "data": [{
                "q": "I'm a quote",
                "a": "Very Great author"
            }]
        }
        quote = get_quote
        print(quote)
        assert quote

