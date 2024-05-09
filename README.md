## Tech Chalenge #1
Repositório com objetivo de atender aos requisitos propostos no projeto integrador do curso de Machine Learning Engineering da instituição FIAP.

## Tecnologias utilizadas
- Python
- FastAPI
- Swagger
- Docker

## Requisitos
- Docker
- Docker Compose

## Deploy
A cada alteração realizada na branch `Master` a pipeline de deploy será acionada, enviando as alterações para o serviço Lambda Serveless, conforme diagrama:

![github-deploy-flow.svg](image%2Fgithub-deploy-flow.svg)

## Comandos
Utilize os comandos abaixo para executar as ações desejadas:

**Iniciar aplicação localmente**

```
docker-compose up -d
```

**Instalar depêndencias do projeto**

```
docker-compose exec web pip install -r ../requirements/requirements.txt
```


**Limpar cache**

```
rm -rf __pycache__
```
## Autenticação

EndPoint Login espera Key 'password' e value 'SenhaFixada' para gerar token de autenticação

Demais EndPoints esperam Key 'Authorization' e Value 'Bearer tokenGerado'
## Documentação
Com o projeto rodando localmente, basta acessar o link para consultar a documentação do projeto:

http://localhost:8000/docs
****

## Agenda evolutiva do projeto:
- [x] Endpoint GET /producao
- [x] Endpoint GET /comercializacao
- [x] Endpoint GET /importacao
- [x] Endpoint GET /exportacao
- [x] Continuous Deploy
- [ ] Acrescentar Payloads de Request e Response na Documentação do Swagger
- [x] Endpoint GET /processamento ***(Necessário corrigir "parseamento" do payload de response)***
- [x] URL pública para API (AWS Lambda)
- [x] Implementar Método de Autenticação (JWT)
- [ ] Testes de integração

# Testes
Após o container subir a api, basta realizar uma requisição nos diferentes endpoints que a api oferece. O notebook "testes.ipynb" contém todos os testes para serem executados apenas rodando as células.
