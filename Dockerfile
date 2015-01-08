FROM ubuntu:trusty

# Set locale to UTF-8
RUN locale-gen en_US.UTF-8
RUN update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8

RUN apt-get update
RUN apt-get dist-upgrade -y

RUN mkdir /root/.pycharm_helpers

# Install and set up SSH
RUN apt-get install -y openssh-server
RUN echo "root:pass" | chpasswd
RUN mkdir /var/run/sshd

# Python 3
RUN apt-get install -y python3 python3-setuptools sqlite3 python3-lxml python3-pillow
RUN apt-get install -y git
RUN easy_install3 pip
RUN pip install Django==1.7.2
# https://code.google.com/p/feedparser/issues/detail?id=403
RUN pip install git+https://code.google.com/p/feedparser/
RUN pip install dateutils==0.6.6
RUN pip install django-allauth==0.19.0
RUN pip install djangorestframework==3.0.2
RUN pip install django-widget-tweaks==1.3
RUN pip install django-haystack==2.3.1
RUN pip install Whoosh==2.6.0
RUN pip install beautifulsoup4==4.3.2
RUN pip install django-debug-toolbar
RUN apt-get install csstidy
RUN pip install slimit
RUN pip install django-pipeline==1.3.24

RUN apt-get install -y postgresql postgresql-client python3-psycopg2
USER postgres
RUN /etc/init.d/postgresql start &&\
    psql --command "CREATE USER mypguser WITH PASSWORD 'pass';" &&\
    createdb -O mypguser mydb

USER root
# Comment out a line from /etc/pam.d/sshd to not get `Connection to 127.0.0.1
# closed. Exit status 254.` when connection to the container over ssh.
RUN sed -i 's/^\(session    required     pam\_loginuid\.so\)/\#\1/' /etc/pam.d/sshd

RUN sed -i 's/^\(PermitRootLogin\) without-password/\1 yes/' /etc/ssh/sshd_config

CMD /usr/sbin/sshd && \
    /etc/init.d/postgresql start && \
    python3 /home/sputnik/app/create_secret_key.py && \
    python3 /home/sputnik/app/manage.py syncdb && \
    bash
