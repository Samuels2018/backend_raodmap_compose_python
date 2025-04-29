FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

RUN python manage.py makemigrations
RUN python manage.py migrate
RUN python manage.py createsuperuser

CMD [ "uvicorn", "app.main:app", "--reload", ]
