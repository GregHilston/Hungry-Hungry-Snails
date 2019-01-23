FROM python:3.7-stretch

MAINTAINER Your Name "Gregory.Hilston@gmail.com"

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

COPY ./requirements.txt /app/requirements.txt 

WORKDIR /app

RUN pip install -r requirements.txt

# This copies our source code down to the container and is why we must rebuild everytime anything in the source code changes
COPY . /app

ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]