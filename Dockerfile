FROM python:3.12-alpine3.19


RUN apk add --no-cache build-base
RUN apk add --no-cache mariadb-dev

WORKDIR /usr/src/app


COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]