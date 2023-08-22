FROM python:3.10

WORKDIR /incident_app

COPY . /incident_app
COPY pyproject.toml /incident_app

RUN touch README.md

ENV PYTHONPATH "${PYTHONPATH}:/incident_app/"
 
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

# Uncomment this part and comment all above in case poetry installation will not work
# WORKDIR /incident_app

# COPY . /incident_app

# RUN pip3 install --no-cache-dir -r requirements.txt

# ENV PYTHONPATH "${PYTHONPATH}:/incident_app/"

EXPOSE 8989

WORKDIR /incident_app/incident_collection

CMD uvicorn main:app --host 0.0.0.0 --port 8989 --reload