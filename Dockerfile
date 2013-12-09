FROM ubuntu:latest

RUN apt-get update
RUN apt-get install -y python3 python3-setuptools sqlite3
RUN easy_install3 django feedparser

RUN cd usr/bin && touch run && echo "#\!sh\npython3 /sputnik/manage.py runserver 0.0.0.0:8000" > run && chmod u+x run && cd -

WORKDIR /sputnik

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
