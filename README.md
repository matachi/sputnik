# Sputnik

Podcast site built with Django.

## Run with Docker

Build the Docker image:

    sudo docker build -t matachi/sputnik .

Run the image:

    sudo docker run -i -t -v `pwd`:`pwd`:rw -p 127.0.0.1:8000:8000 -p 127.0.0.1:1337:22 matachi/sputnik

In the container, `cd` into the project folder, which is located at the same
path as on the host. Then start the Django development web server with:

    python3 manage.py runserver 0.0.0.0:8000

## Configure PyCharm

To work with the project in PyCharm and still run it in Docker, read the
following text.

Set your project Python interpreter to a remote interpreter. Configure it with
the following settings:

    Host: 127.0.0.1
    Port: 1337
    Username: root
    Auth type: Password
    Password: pass
    Python interpreter path: /usr/bin/python3
    PyCharm helpers path: /root/pycharm_helpers

And before starting a *Django server*, configure the host IP to `0.0.0.0:8000`.
