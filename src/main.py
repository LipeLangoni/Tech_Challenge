from fastapi import FastAPI
from scrapping import DirectScrapper
from mangum import Mangum

scrap = DirectScrapper()

app = FastAPI()

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
