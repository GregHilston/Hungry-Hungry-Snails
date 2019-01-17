FROM python:3.7-stretch

MAINTAINER Your Name "Gregory.Hilston@gmail.com"

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

COPY ./requirements.txt /app/requirements.txt 

WORKDIR /app

RUN pip install -r requirements.txt

# We copy just the requirements.txt first to leverage Docker cache (for production)

# user either COPY or VOLUME. COPY is best for production and VOLUMNE is best for development (don't have to rebuild container each src code change)
COPY . /app

# VOLUME . /app

ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]