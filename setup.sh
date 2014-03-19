#!/usr/bin/env bash

# Python
echo -e "\ndeb http://http.debian.net/debian testing main" >> /etc/apt/sources.list
echo "Package: *
Pin: release a=stable
Pin-Priority: 600

Package: *
Pin: release a=testing
Pin-Priority: 550" > /etc/apt/preferences
apt-get update
apt-get install -y -t testing python3 python3-pip

# Virtualenv
pip3 install virtualenv
virtualenv -p /usr/bin/python3 env
source env/bin/activate

# Django site dependencies
apt-get install -y libjpeg-dev zlib1g-dev
pip install Pillow
apt-get install -y -t testing libxml2-dev libxslt1-dev
pip install lxml
pip install django
pip install feedparser
pip install dateutils
pip install django-allauth
pip install djangorestframework
pip install django-widget-tweaks
pip install django-haystack Whoosh
pip install beautifulsoup4
pip install South
pip install django-debug-toolbar
apt-get install csstidy
pip install slimit django-pipeline

# PostgreSQL
apt-get install -y postgresql postgresql-client
apt-get install libpq-dev
pip install psycopg2
/etc/init.d/postgresql start &&\
    sudo -u postgres psql --command "CREATE USER mypguser WITH PASSWORD 'pass';" &&\
    sudo -u postgres createdb -O mypguser mydb

# Nginx
apt-get intall -y nginx
/etc/init.d/nginx start
ln -s /sputnik/conf/nginx.conf /etc/nginx/sites-enabled/

# uWSGI
apt-get install libpcre3-dev
pip install uwsgi
chown -R www-data:www-data `pwd`
mkdir /var/log/uwsgi/
touch /var/log/uwsgi/log.log
chown -R www-data:www-data /var/log/uwsgi/

# Django
python3 manage.py collectstatic
