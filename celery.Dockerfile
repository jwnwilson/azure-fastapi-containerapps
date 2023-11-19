FROM python:3.7-slim

ENV DOCKER=true

COPY pyproject.toml .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir poetry && \
    poetry install

COPY . /app

CMD ["poetry", "run", "celery", "-A", "app.app.worker.celery_worker", "worker", "-l", "info", "-Q", "test-queue", "-c", "1"]