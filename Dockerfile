FROM stackbrew/ubuntu:13.10

RUN apt-get update

RUN mkdir /root/.pycharm_helpers

# Install and set up SSH
RUN apt-get install -y openssh-server
RUN echo "root:pass" | chpasswd
RUN mkdir /var/run/sshd

RUN apt-get install -y python3 python3-setuptools sqlite3 python3-lxml python3-pillow
RUN easy_install3 pip
RUN pip install django feedparser
RUN pip install dateutils
# Install django-allauth, issue: https://github.com/pennersr/django-allauth/issues/475
RUN pip install https://github.com/willhoag/django-allauth/tarball/49ceb777b3917ee5640a5e304698b9ca9cd11887
RUN pip install djangorestframework
RUN pip install django-widget-tweaks
RUN pip install django-haystack Whoosh
RUN pip install beautifulsoup4

# Comment out a line from /etc/pam.d/sshd to not get `Connection to 127.0.0.1
# closed. Exit status 254.` when connection to the container over ssh.
RUN sed -i 's/^\(session    required     pam\_loginuid\.so\)/\#\1/' /etc/pam.d/sshd

CMD /usr/sbin/sshd && bash
