import logging
import unittest
from unittest.mock import Mock
from unittest.mock import patch

from fastapi import status

from src.scrapping.scrapping import DirectScrapper


class TestDirectScrapper(unittest.TestCase):

    BASE_URL = 'http://test.com'

    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName)

    @patch('requests.get')
    def test_get_data_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = status.HTTP_200_OK
        mock_response.content = b'col1,col2\n1,2\n3,4'
        mock_get.return_value = mock_response

        scrapper = DirectScrapper()
        response = scrapper.get_data(self.BASE_URL, 'utf-8', ',')

        expect_response = [{'col1': 1, 'col2': 2}, {'col1': 3, 'col2': 4}]

        self.assertEqual(response, expect_response)

    @patch('requests.get')
    def test_get_data_failed(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = status.HTTP_504_GATEWAY_TIMEOUT
        mock_response.content = None
        mock_get.return_value = mock_response

        scrapper = DirectScrapper()

        with self.assertLogs(level=logging.getLevelName(logging.ERROR)) as log:
            response = scrapper.get_data(self.BASE_URL, 'utf-8', ',')

        self.assertIsNone(response)
        self.assertIn('Fail to download data', log.output[0])
