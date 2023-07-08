FROM python:3.9-slim-buster as python-base

WORKDIR /app

COPY poetry.lock .
COPY pyproject.toml .

RUN apt-get update && \
    apt-get install -y python3-pip git

RUN pip install poetry

COPY . .

RUN poetry install

CMD ["poetry", "run", "uvicorn", "src.service_markets.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
