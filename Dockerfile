FROM ubuntu:latest

RUN apt-get update

RUN mkdir /root/.pycharm_helpers

# Install and set up SSH
RUN apt-get install -y openssh-server
RUN echo "root:pass" | chpasswd
RUN mkdir /var/run/sshd

RUN apt-get install -y python3 python3-setuptools sqlite3
RUN easy_install3 pip
RUN pip install django feedparser
RUN pip install dateutils
# Install django-allauth, issue: https://github.com/pennersr/django-allauth/issues/475
RUN pip install https://github.com/willhoag/django-allauth/tarball/49ceb777b3917ee5640a5e304698b9ca9cd11887

CMD /usr/sbin/sshd && bash
