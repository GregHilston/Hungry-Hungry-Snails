# Since we're using COPY in our Dockerfile, we have to run build everytime our sources code changes

docker build -t hungry-hungry-snails:latest .