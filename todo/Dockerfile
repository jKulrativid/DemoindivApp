FROM python:3.9

WORKDIR /code

RUN apt-get update

COPY ./requirements.txt /code/requirements.txt

RUN python -m pip install --upgrade pip

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code/app

ENV PYTHONPATH="${PYTHONPATH}:/code/app"

ENTRYPOINT [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080" ]
