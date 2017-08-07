FROM python:3

WORKDIR /var/app

ADD addressbook.proto .

RUN apt-get update && apt-get install unzip 

ADD requirements.txt .
RUN pip install -r requirements.txt

ADD . .

CMD ["/var/app/start-services.sh"]
