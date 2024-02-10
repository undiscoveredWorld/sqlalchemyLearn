FROM python:3.10-alpine3.19

WORKDIR /app

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /app/src

EXPOSE 8080

ENV DOCKER_MODE=True

CMD uvicorn main:app --host 0.0.0.0 --port 8080