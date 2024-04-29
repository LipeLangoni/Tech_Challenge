from fastapi import FastAPI
from src.scrapping.scrapping import DirectScrapper
from fastapi.responses import JSONResponse
from mangum import Mangum

scrap = DirectScrapper()
app = FastAPI()


@app.get("/")
async def welcome():
    return JSONResponse({
        'message': 'Welcome to Tech Challenge | Group #58 API! Check out /docs to see our resources'
    })


@app.get("/producao")
async def get_producao():
    return scrap.get_data("http://vitibrasil.cnpuv.embrapa.br/download/Producao.csv")


@app.get("/processamento")
async def get_processamento():
    return scrap.get_data("http://vitibrasil.cnpuv.embrapa.br/download/ProcessaViniferas.csv")


@app.get("/comercializacao")
async def get_comercializacao():
    return scrap.get_data("http://vitibrasil.cnpuv.embrapa.br/download/Comercio.csv")


@app.get("/importacao")
async def get_importacao():
    return scrap.get_data("http://vitibrasil.cnpuv.embrapa.br/download/ImpVinhos.csv")


@app.get("/exportacao")
async def get_exportacao():
    return scrap.get_data("http://vitibrasil.cnpuv.embrapa.br/download/ExpVinho.csv")

handler = Mangum(app)