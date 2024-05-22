import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer
import jwt
from jwt.exceptions import PyJWTError
from datetime import datetime, timedelta
from src.scrapping.scrapping import DirectScrapper
from fastapi.responses import JSONResponse
from mangum import Mangum
from pydantic import BaseModel
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse
from fastapi.encoders import jsonable_encoder

scrap = DirectScrapper()
app = FastAPI(openapi_prefix=f'{os.getenv("STAGE")}')
#app = FastAPI()


class ProducaoResponse(BaseModel):
    producao: list

class ProcessamentoResponse(BaseModel):
    processamento: list

class ComercializacaoResponse(BaseModel):
    comercializacao: list

class ImportacaoResponse(BaseModel):
    importacao: list

class ExportacaoResponse(BaseModel):
    exportacao: list




# Chave secreta para assinar o JWT
SECRET_KEY = "testando"
# Algoritmo de criptografia para o JWT
ALGORITHM = "HS256"
# Tempo de expiração do JWT (em minutos)
ACCESS_TOKEN_EXPIRE_MINUTES = 30
# Senha Fixa para conseguir Token
FIXED_PASSWORD = "senhafixa"
# Instância do esquema de autenticação HTTPBearer
security = HTTPBearer()


# Função para gerar o token JWT
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Rota de login para obter o token JWT
@app.post("/login")
async def login(password: str):
    if password != FIXED_PASSWORD:
        raise HTTPException(status_code=401, detail="Senha incorreta")

    token = create_access_token({"sub": "token_de_acesso"})
    return {"access_token": token}


# Função de autenticação
async def authenticate(token:str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload["sub"] != "token_de_acesso":
            return False    
    except PyJWTError:
        return False
    return True


@app.get("/", response_class=HTMLResponse)
async def welcome():
     return get_swagger_ui_html(openapi_url="openapi.json", title="Welcome to My API")


@app.post("/producao", response_model=ProducaoResponse)
async def get_producao(token:str):

    if await authenticate(token):
        producao_data = scrap.get_data("http://vitibrasil.cnpuv.embrapa.br/download/Producao.csv", "utf-8", ";")
        return JSONResponse(content=jsonable_encoder({"producao": producao_data}))
    else:
        raise HTTPException(status_code=403, detail="Token inválido")


@app.post("/processamento", response_model=ProcessamentoResponse)
async def get_processamento(token:str):
    if await authenticate(token):
        return JSONResponse(content=jsonable_encoder({"processamento":scrap.get_data("http://vitibrasil.cnpuv.embrapa.br/download/ProcessaViniferas.csv","utf-8","\t")}))
    else:
        raise HTTPException(status_code=403, detail="Token inválido")


@app.post("/comercializacao", response_model=ComercializacaoResponse)
async def get_comercializacao(token:str):
    if await authenticate(token):
        return JSONResponse(content=jsonable_encoder({"comercializacao":scrap.get_data("http://vitibrasil.cnpuv.embrapa.br/download/Comercio.csv","utf-8",";")}))
    else:
        raise HTTPException(status_code=403, detail="Token inválido")


@app.post("/importacao", response_model=ImportacaoResponse)
async def get_importacao(token:str):
    if await authenticate(token):
        return JSONResponse(content=jsonable_encoder({"importacao":scrap.get_data("http://vitibrasil.cnpuv.embrapa.br/download/ImpVinhos.csv","utf-8",";")}))
    else:
        raise HTTPException(status_code=403, detail="Token inválido")


@app.post("/exportacao", response_model=ExportacaoResponse)
async def get_exportacao(token:str):
    if await authenticate(token):
        return JSONResponse(content=jsonable_encoder({"exportacao":scrap.get_data("http://vitibrasil.cnpuv.embrapa.br/download/ExpVinho.csv","utf-8",";")}))
    else:
        raise HTTPException(status_code=403, detail="Token inválido")

@app.get("/docs", include_in_schema=False, response_class=HTMLResponse)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(openapi_url="openapi.json", title="Custom Swagger UI")



handler = Mangum(app)
