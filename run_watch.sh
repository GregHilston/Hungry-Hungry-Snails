# creates a container and then starts it. To be used the first time.
docker run --name hungry-hungry-snails -it -p 5000:5000 -v ~/Git/Hungry-Hungry-Snails:/app -e FLASK_DEBUG=1 hungry-hungry-snails