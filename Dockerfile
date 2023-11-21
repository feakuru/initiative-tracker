FROM python:3.12-slim
WORKDIR /app
RUN apt update
RUN apt --assume-yes upgrade
RUN apt --assume-yes install build-essential

COPY initiative_tracker /app/initiative_tracker
COPY pyproject.toml poetry.lock README.md /app/
RUN python -m pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --only main

EXPOSE 8888
WORKDIR /app/initiative_tracker
CMD ["uvicorn", "main:app", "--port=8888", "--host=0.0.0.0"]
