from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from jwt.exceptions import PyJWTError
from datetime import datetime, timedelta
from src.scrapping.scrapping import DirectScrapper
from fastapi.responses import JSONResponse
from mangum import Mangum

scrap = DirectScrapper()
app = FastAPI(openapi_prefix='/default/')


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


@app.get("/")
async def welcome():
    return JSONResponse({
        'message': 'Welcome to Tech Challenge | Group #58 API! Check out /docs to see our resources'
    })


@app.get("/producao", dependencies=[Depends(authenticate)])
async def get_producao():
    return scrap.get_data("http://vitibrasil.cnpuv.embrapa.br/download/Producao.csv","utf-8",";")


@app.get("/processamento", dependencies=[Depends(authenticate)])
async def get_processamento():
    return scrap.get_data("http://vitibrasil.cnpuv.embrapa.br/download/ProcessaViniferas.csv","utf-8","\t")


@app.get("/comercializacao", dependencies=[Depends(authenticate)])
async def get_comercializacao():
    return scrap.get_data("http://vitibrasil.cnpuv.embrapa.br/download/Comercio.csv","utf-8",";")


@app.get("/importacao", dependencies=[Depends(authenticate)])
async def get_importacao():
    return scrap.get_data("http://vitibrasil.cnpuv.embrapa.br/download/ImpVinhos.csv","utf-8",";")


@app.get("/exportacao", dependencies=[Depends(authenticate)])
async def get_exportacao():
    return scrap.get_data("http://vitibrasil.cnpuv.embrapa.br/download/ExpVinho.csv","utf-8",";")


handler = Mangum(app)
