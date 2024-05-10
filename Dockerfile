FROM python:3.10-slim

WORKDIR /app

COPY . /app

ENV STAGE=""

RUN pip install -r requirements/requirements.txt --ignore-installed

WORKDIR /app

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]