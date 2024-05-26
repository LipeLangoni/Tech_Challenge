from unittest.mock import AsyncMock

import pytest
from fastapi import status
from httpx import ASGITransport
from httpx import AsyncClient

from src.main import app
from src.scrapping.scrapping import DirectScrapper


@pytest.fixture
def mock_scrapper(mocker):
    mocker.patch.object(DirectScrapper, 'get_data', return_value=[{'column1': 'value1', 'column2': 'value2'}])


@pytest.fixture
def mock_jwt_decode(mocker):
    return mocker.patch('jwt.decode', return_value={'sub': 'token_de_acesso'})


def data_provider_available_resources():
    data = [
        {'resource': 'producao'},
        {'resource': 'processamento'},
        {'resource': 'comercializacao'},
        {'resource': 'importacao'},
        {'resource': 'exportacao'}
    ]

    for row in data:
        yield row


class TestMain:
    BASE_URL = 'http://test.com'
    TOKEN = 'test_token'

    @pytest.fixture(params=data_provider_available_resources())
    def data_provider(self, request):
        return request.param

    @pytest.mark.asyncio
    async def test_welcome(self):
        async with AsyncClient(transport=ASGITransport(app=app)) as ac:
            response = await ac.get(f'{self.BASE_URL}/')
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.asyncio
    async def test_get_resources_without_auth_token(self, mock_scrapper, data_provider):
        async with AsyncClient(transport=ASGITransport(app=app)) as ac:
            path = data_provider['resource']
            response = await ac.get(f'{self.BASE_URL}/{path}')

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert response.json() == {'detail': 'Not authenticated'}

    @pytest.mark.asyncio
    async def test_get_resources(self, mock_jwt_decode, mock_scrapper, mocker, data_provider):
        mocker.patch('src.main.authenticate', AsyncMock(return_value=True))

        async with AsyncClient(transport=ASGITransport(app=app)) as ac:
            resource = data_provider['resource']
            headers = {'Authorization': f'Bearer {self.TOKEN}'}

            response = await ac.get(f'{self.BASE_URL}/{resource}', headers=headers)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {f'{resource}': [{'column1': 'value1', 'column2': 'value2'}]}


if __name__ == '__main__':
    pytest.main()  # pragma: no cover
