FROM ubuntu:latest

RUN apt-get update

RUN mkdir /root/.pycharm_helpers

# Install and set up SSH
RUN apt-get install -y openssh-server
RUN echo "root:pass" | chpasswd
RUN mkdir /var/run/sshd

RUN apt-get install -y python3 python3-setuptools sqlite3
RUN easy_install3 pip
RUN pip install django feedparser dateutils

CMD /usr/sbin/sshd && bash
