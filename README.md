# Sputnik

Podcast aggregator built with Django.

Author: Daniel Jonsson  
License: [MIT License](LICENSE)

## Run with Docker

Build the Docker image:

    $ sudo docker build -t matachi/sputnik .

Run the image:

    $ sudo docker run -i -t -v `pwd`:/home/sputnik/app:rw -p 80:8000 -p 1337:22 matachi/sputnik

Then, inside the container, start the Django development web server:

    $ python3 /home/sputnik/app/manage.py runserver 0.0.0.0:8000

Finally open [localhost](http://localhost) in the web browser.

## Load sample data

Add a few podcasts to the database:

    $ python3 manage.py loaddata sample_podcasts

Fetch the metadata about these podcasts from their RSS feeds:

    $ python3 manage.py updatepodcasts

Fetch the podcasts' episodes:

    $ ./update.sh

## Backup database

Make an SQL dump:

    $ pg_dump mydb -U mypguser -h localhost > database.sql

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

And before starting a *Django server*, make the following configurations:

    Host: 0.0.0.0
    Port: 8000
    Path mappings: /path/to/sputnik/on/host=/home/sputnik/app

Where `/path/to/sputnik/on/host` is the directory on the host where this
project directory is located.

## Load development data

**TODO** Update this section.

To automatically setup the development area in the Docker container with sample
podcasts etc you can run the fabfile, which will execute the necessary
commands. First you need to have Fabric installed:

    $ sudo apt-get install fabric

Note that Fabric is only supported under Python 2.7. Then run:

    $ fab setup_dev

## Fabric commands

**TODO** Update this section.

* `setup_dev` will load sample podcasts, update the podcasts, fetch episodes
  etc.
* `update_podcasts` will run `python3 manager.py updatepodcasts` in the
  container.
* `rebuild_index` will rebuild the search index.

## Production and live server

### Setup

Ubuntu setup script:

    $ ./setup.sh

### Controlling nginx and uWSGI

**TODO** Update this section.

* <http://nginx.org/en/docs/control.html>
* <http://uwsgi-docs.readthedocs.org/en/latest/Management.html>

    /etc/init.d/nginx start
    /etc/init.d/nginx restart
    kill -s SIGINT `cat mysite.pid`
    source env/bin/activate
    uwsgi --ini conf/uwsgi.ini
    uwsgi --reload mysite.pid
    uwsgi --stop mysite.pid

### Upgrade PyPI packages

**TODO** Update this section.

<http://stackoverflow.com/questions/2720014/upgrading-all-packages-with-pip>:

    pip freeze --local | grep -v '^\-e' | cut -d = -f 1  | xargs pip install -U
