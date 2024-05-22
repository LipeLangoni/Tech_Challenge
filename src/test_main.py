import pytest
from httpx import AsyncClient
from main import app
from src.scrapping.scrapping import DirectScrapper
from unittest.mock import Mock

@pytest.fixture
def mock_scrapper(mocker):
    mocker.patch.object(DirectScrapper, 'get_data', return_value=[{'column1': 'value1', 'column2': 'value2'}])

@pytest.mark.asyncio
async def test_welcome():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {
        'message': 'Welcome to Tech Challenge | Group #58 API! Check out /docs to see our resources'
    }

@pytest.mark.asyncio
async def test_get_producao(mock_scrapper):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/producao")
    assert response.status_code == 200
    assert response.json() == [{'column1': 'value1', 'column2': 'value2'}]

# Adicione testes para outras rotas da mesma forma
@pytest.mark.asyncio
async def test_get_processamento(mock_scrapper):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/processamento")
    assert response.status_code == 200
    assert response.json() == [{'column1': 'value1', 'column2': 'value2'}]

@pytest.mark.asyncio
async def test_get_comercializacao(mock_scrapper):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/comercializacao")
    assert response.status_code == 200
    assert response.json() == [{'column1': 'value1', 'column2': 'value2'}]

@pytest.mark.asyncio
async def test_get_importacao(mock_scrapper):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/importacao")
    assert response.status_code == 200
    assert response.json() == [{'column1': 'value1', 'column2': 'value2'}]

@pytest.mark.asyncio
async def test_get_exportacao(mock_scrapper):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/exportacao")
    assert response.status_code == 200
    assert response.json() == [{'column1': 'value1', 'column2': 'value2'}]
