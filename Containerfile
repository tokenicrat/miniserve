FROM quay.io/lib/python:3.13-alpine

WORKDIR /app

COPY src/app.py src/gunicorn.conf.py src/wsgi.py requirements.txt /app/
RUN pip install -r requirements.txt --no-cache-dir

RUN mkdir /data

EXPOSE 5000

CMD ["gunicorn", "--config", "gunicorn.conf.py", "wsgi:application"]
