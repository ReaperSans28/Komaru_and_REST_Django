FROM python:3.12

WORKDIR /lms

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock ./

RUN pip install poetry && \
poetry install --no-root

COPY . .

EXPOSE 8000