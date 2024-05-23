import os
from datetime import datetime, timedelta

from fastapi import FastAPI, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from mangum import Mangum
import jwt
from jwt.exceptions import PyJWTError

from src.scrapping.scrapping import DirectScrapper
from src.responses.producao_response import ProducaoResponse
from src.responses.processamento_response import ProcessamentoResponse
from src.responses.exportacao_response import ExportacaoResponse
from src.responses.importacao_response import ImportacaoResponse
from src.responses.comercializacao_response import ComercializacaoResponse

scrap = DirectScrapper()
app = FastAPI(openapi_prefix=f'{os.getenv("STAGE")}')

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
     return get_swagger_ui_html(openapi_url="src/openapi.json", title="Welcome to My API")


@app.get("/producao", dependencies=[Depends(authenticate)],response_model=ProducaoResponse)
async def get_producao():
    producao_data = scrap.get_data("http://vitibrasil.cnpuv.embrapa.br/download/Producao.csv", "utf-8", ";")
    return JSONResponse(content=jsonable_encoder({"producao": producao_data}))
    


@app.get("/processamento", dependencies=[Depends(authenticate)],response_model=ProcessamentoResponse)
async def get_processamento():
    return JSONResponse(content=jsonable_encoder({"processamento":scrap.get_data("http://vitibrasil.cnpuv.embrapa.br/download/ProcessaViniferas.csv","utf-8","\t")}))
    


@app.get("/comercializacao", dependencies=[Depends(authenticate)],response_model=ComercializacaoResponse)
async def get_comercializacao():
    return JSONResponse(content=jsonable_encoder({"comercializacao":scrap.get_data("http://vitibrasil.cnpuv.embrapa.br/download/Comercio.csv","utf-8",";")}))



@app.get("/importacao", dependencies=[Depends(authenticate)],response_model=ImportacaoResponse)
async def get_importacao():
    return JSONResponse(content=jsonable_encoder({"importacao":scrap.get_data("http://vitibrasil.cnpuv.embrapa.br/download/ImpVinhos.csv","utf-8",";")}))



@app.get("/exportacao", dependencies=[Depends(authenticate)],response_model=ExportacaoResponse)
async def get_exportacao():
    return JSONResponse(content=jsonable_encoder({"exportacao":scrap.get_data("http://vitibrasil.cnpuv.embrapa.br/download/ExpVinho.csv","utf-8",";")}))


@app.get("/docs", include_in_schema=False, response_class=HTMLResponse)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(openapi_url="openapi.json", title="Custom Swagger UI")



handler = Mangum(app)
