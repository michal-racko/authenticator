FROM python:3.9-buster

COPY src /opt/authenticator
WORKDIR /opt/authenticator

COPY requirements.txt /opt/authenticator/
RUN pip install -r requirements.txt

EXPOSE 8000

CMD python manage.py migrate && uwsgi authenticator.ini