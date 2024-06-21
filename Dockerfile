FROM python:3.10-alpine

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONBUFFERED=1

RUN adduser --disabled-password --gecos '' PrioritySoft

WORKDIR /project

COPY . /project

RUN chown -R PrioritySoft:PrioritySoft /project

COPY requirements.txt requirements.txt

RUN pip3 install -r /project/requirements.txt

RUN pip3 install supervisor

EXPOSE 8000

USER PrioritySoft

RUN mkdir -p /project/static

RUN chown -R PrioritySoft:PrioritySoft /project/static

CMD supervisorctl reread && supervisorctl update && python manage.py wait_for_db && python manage.py makemigrations && python manage.py migrate && python manage.py collectstatic --noinput && supervisord -c /project/supervisord.conf
