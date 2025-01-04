# syntax=docker/dockerfile:1
   
FROM python:3.9

WORKDIR /Ijobs

COPY . .

RUN apt-get update && apt-get install -y postgresql-client

RUN pip install --no-cache --upgrade -r /Ijobs/requirements.txt

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "trace", "--workers", "1"]
