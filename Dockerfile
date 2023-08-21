FROM python:3.10

RUN mkdir /app

COPY . /app
COPY pyproject.toml /app

WORKDIR /app
RUN touch README.md

ENV PYTHONPATH=${PYTHONPATH}:${PWD}
 
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

WORKDIR /app/incident-collection

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]