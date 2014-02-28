#!/usr/bin/env bash

echo -e "\ndeb http://http.debian.net/debian testing main" >> /etc/apt/sources.list
echo -e "Package: *\nPin: release a=testing\nPin-Priority: -10" > /etc/apt/preferences
apt-get update
apt-get install -y -t testing python3 python3-pip
pip3 install virtualenv
virtualenv -p /usr/bin/python3 env
source env/bin/activate
apt-get install -y libjpeg-dev zlib1g-dev
pip install Pillow
apt-get install -y -t testing libxml2-dev libxslt1-dev
pip3 install lxml
pip3 install django
pip3 install feedparser
pip3 install dateutils
pip3 install django-allauth
pip3 install djangorestframework
pip3 install django-widget-tweaks
pip3 install django-haystack Whoosh
pip3 install beautifulsoup4
pip3 install django-debug-toolbar

apt-get install -y postgresql postgresql-client
apt-get install libpq-dev
pip3 install psycopg2
/etc/init.d/postgresql start &&\
    sudo -u postgres psql --command "CREATE USER mypguser WITH PASSWORD 'pass';" &&\
    sudo -u postgres createdb -O mypguser mydb
