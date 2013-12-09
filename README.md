# Sputnik

Podcast site built with Django.

## Run with Docker

Build the Docker image:

    sudo docker build -t matachi/sputnik .

Run the image:

    sudo docker run -i -t -v `pwd`:/sputnik/:rw -p 127.0.0.1:8000:8000 matachi/sputnik bash

Easily start the Django development web server inside the Docker container with
`run`. Then open <http://127.0.0.1:8000> in the web browser.
