FROM ubuntu:latest

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y --no-install-recommends -y build-essential
RUN apt-get install -y --no-install-recommends python3 python3-pip
RUN pip3 install pipenv


RUN apt-get install -y python3
RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev



COPY Pipfile .
COPY Pipfile.lock .
RUN pipenv install --system --deploy
RUN pipenv run pip install psycopg2-binary
RUN pipenv install drf-yasg
RUN pipenv install django
RUN pipenv install tzdata
RUN pipenv run pip install gunicorn
RUN apt-get install -y nginx
COPY . .

CMD ["pipenv", "run", "gunicorn", "-b", "0.0.0.0:8080", "CarDealership.wsgi:application"]

