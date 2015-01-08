#!/usr/bin/env bash

# Init
aptitude update
aptitude full-upgrade -y
adduser deploy
adduser deploy sudo
sudo -u deploy mkdir -p /home/deploy/sputnik
cd /home/deploy/sputnik

# Python
aptitude install python3-pip

# Virtualenv
pip3 install virtualenv
sudo -u deploy virtualenv env
source env/bin/activate

# Django site dependencies
aptitude install -y libjpeg-dev zlib1g-dev
pip install Pillow==2.4.0

aptitude install -y libxml2-dev libxslt1-dev
pip install lxml==3.3.5

pip install Django==1.7.2
pip install feedparser==5.1.3
pip install dateutils==0.6.6
pip install django-allauth==0.19.0
pip install djangorestframework==3.0.2
pip install django-widget-tweaks==1.3
pip install django-haystack==2.3.1
pip install Whoosh==2.6.0
pip install beautifulsoup4==4.3.2

#apt-get install csstidy
#pip install slimit
pip install django-pipeline==1.3.24

chown -R deploy:deploy env

# Django
python3 manage.py collectstatic

# PostgreSQL
aptitude install -y postgresql postgresql-client
aptitude install -y libpq-dev
pip install psycopg2
/etc/init.d/postgresql start &&\
    sudo -u postgres psql --command "CREATE USER mypguser WITH PASSWORD 'pass';" &&\
    sudo -u postgres createdb -O mypguser mydb

# Nginx
aptitude install -y nginx
service nginx start
ln -s /home/deploy/sputnik/conf/nginx.conf /etc/nginx/sites-enabled/

# uWSGI
sudo -u deploy mkdir -p /home/deploy/uwsgi
cd /home/deploy/uwsgi

deactivate
sudo -u deploy virtualenv env
source env/bin/activate

aptitude install -y libpcre3-dev
pip install uwsgi
chown -R deploy:deploy env

sudo -u deploy mkdir log
