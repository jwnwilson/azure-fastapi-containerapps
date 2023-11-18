FROM python:3.7-slim

ENV DOCKER=true

COPY pyproject.toml .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir poetry && \
    poetry install

COPY . /app

EXPOSE 80

CMD ["poetry", "run", "hypercorn", "app/app/main:app", "--bind", "0.0.0.0:80", "--reload"]