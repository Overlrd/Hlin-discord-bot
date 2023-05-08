import datetime
import pytest
import json
from unittest import mock
import logging
import requests

from hlin.utils.quote_utils import post_quote , get_quote , get_quote_from_db


@pytest.fixture
def expected_single_doc():
    """Represent a single doc the post_quote func will send to db"""
    return  {
            "author": "Author 1",
            "quote": "Quote 1",
            "date": "22:01:01:12:00:00"
        }

@pytest.fixture
def expected_many_docs():
    """Represent a multiple doc the post_quote func will send to db"""
    return  [
            {
                "author": "Author 1",
                "quote": "Quote 1",
                "date": "22:01:01:12:00:00"
            },
            {
                "author": "Author 2",
                "quote": "Quote 2",
                "date": "22:01:01:12:00:00"
            }
        ]



class TestQuoteUtils:
    """Test quote_utils functions \n- post_quote \n- get_quote \n- get_quote from db"""

    def test_post_quote(self,expected_single_doc,expected_many_docs):
        """Test post_quote function from quote_utils \n 
        Mocked quotes_collection \n 
        assert 'insert_one' and 'insert_many' called successfully 
        """
        # Mocking the quotes_collection for testing purposes
        quotes_collection = mock.MagicMock()

        # Mocking datetime.datetime.now() to return a fixed date and time
        mock_datetime = mock.Mock(wraps=datetime.datetime)
        mock_datetime.now.return_value = datetime.datetime(2022, 1, 1, 12, 0, 0)

        # Patching quotes_collection and datetime.datetime.now() for testing
        with mock.patch('hlin.utils.quote_utils.quotes_collection', quotes_collection), \
            mock.patch('hlin.utils.quote_utils.datetime.datetime', mock_datetime):
            # Call the function with sample quotes
            post_quote(("Author 1", "Quote 1"), ("Author 2", "Quote 2"))
            post_quote(("Author 1", "Quote 1"))


        # Assert the expected calls to quotes_collection.insert_one and quotes_collection.insert_many
        quotes_collection.insert_one.assert_called_once_with(expected_single_doc)
        quotes_collection.insert_many.assert_called_once_with(expected_many_docs)

    def test_get_quote(self):
        """Test get_quote function from quote_utils \n 
        Mocked requests.get value \n 
        assert returned quote == 'Test Quote - Test Author' 
        """

        # Mocking the response for testing purposes
        response_json = [{"q": "Test Quote", "a": "Test Author"}]
        response_text = json.dumps(response_json)
        response_mock = requests.Response()
        response_mock._content = response_text.encode()

        # Patching the requests.get function to return the mocked response
        with mock.patch('requests.get', return_value=response_mock):
            quote = get_quote()
            assert quote == "Test Quote - Test Author"

    def test_get_quote_from_db(self):
        """Test get_quote_from_db function from quote_utils \n 
        Mocked quotes_collection value \n 
        assert returned quote == 'Test Quote - Test Author' 
        """
        quotes_collection = mock.MagicMock()
        quotes_collection.aggregate.return_value = [{"quote": "Test Quote", "author": "Test Author"}]
        with mock.patch('hlin.utils.quote_utils.quotes_collection', quotes_collection):
            quote = get_quote_from_db()
        assert quote == "Test Quote - Test Author"