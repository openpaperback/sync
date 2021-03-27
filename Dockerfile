FROM python:3.8

RUN apt-get install curl
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

WORKDIR /app

COPY poetry.lock .
COPY poetry.toml .
COPY pyproject.toml .

RUN $HOME/.poetry/bin/poetry install

COPY sync sync
COPY startup.py .

CMD $HOME/.poetry/bin/poetry run python startup.py