import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
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
from fastapi.openapi.utils import get_openapi

scrap = DirectScrapper()
# app = FastAPI(openapi_prefix=f'/{os.getenv("STAGE")}')
app = FastAPI()


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
async def authenticate(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        if payload["sub"] != "token_de_acesso":
            raise HTTPException(status_code=403, detail="Token inválido")
    except PyJWTError:
        raise HTTPException(status_code=403, detail="Token inválido")
    return True


@app.get("/", response_class=HTMLResponse)
async def welcome():
     return get_swagger_ui_html(openapi_url="openapi.json", title="Welcome to My API")

# @app.on_event("startup")
# async def generate_openapi_json():
#     with open("openapi.json", "w") as file:
#         json.dump(get_openapi(title="Your API's Title", version="1.0.0", routes=app.routes), file)


@app.get("/producao", dependencies=[Depends(authenticate)],response_model=ProducaoResponse)
async def get_producao():
    producao_data = scrap.get_data("http://vitibrasil.cnpuv.embrapa.br/download/Producao.csv", "utf-8", ";")
    return JSONResponse(content=jsonable_encoder({"producao": producao_data}))


@app.get("/processamento", dependencies=[Depends(authenticate)],response_model=ProcessamentoResponse)
async def get_processamento():
    return {"processamento":scrap.get_data("http://vitibrasil.cnpuv.embrapa.br/download/ProcessaViniferas.csv","utf-8","\t")}


@app.get("/comercializacao", dependencies=[Depends(authenticate)],response_model=ComercializacaoResponse)
async def get_comercializacao():
    return {"comercializacao":scrap.get_data("http://vitibrasil.cnpuv.embrapa.br/download/Comercio.csv","utf-8",";")}


@app.get("/importacao", dependencies=[Depends(authenticate)],response_model=ImportacaoResponse)
async def get_importacao():
    return {"importacao":scrap.get_data("http://vitibrasil.cnpuv.embrapa.br/download/ImpVinhos.csv","utf-8",";")}


@app.get("/exportacao", dependencies=[Depends(authenticate)],response_model=ExportacaoResponse)
async def get_exportacao():
    return {"exportacao":scrap.get_data("http://vitibrasil.cnpuv.embrapa.br/download/ExpVinho.csv","utf-8",";")}

@app.get("/docs", include_in_schema=False, response_class=HTMLResponse)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(openapi_url="openapi.json", title="Custom Swagger UI")



handler = Mangum(app)
