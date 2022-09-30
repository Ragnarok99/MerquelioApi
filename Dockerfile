FROM python:3.9-alpine
ENV ROOT_DIR=/code

WORKDIR $ROOT_DIR
# ENV FLASK_APP=app.py
# ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt

RUN apk add build-base
RUN apk add --no-cache supervisor \
    && python -m pip install --upgrade pip \
    && pip install -r /code/requirements.txt
EXPOSE 8080
COPY . .
ENTRYPOINT ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
