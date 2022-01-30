FROM python:3.8

WORKDIR /code

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code/app