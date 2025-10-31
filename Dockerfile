FROM python:3.12-slim

RUN pip install --no-cache-dir poetry

WORKDIR /data

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

COPY . .

EXPOSE 3000

CMD ["python", "main.py","--debug"]
