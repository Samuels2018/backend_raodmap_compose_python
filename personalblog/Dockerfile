FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN python -m venv .venv
RUN .venv/bin/activate
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN python manage.py makemigrations
RUN python manage.py migrate

CMD [ "python", "manage.py", "runserver", ]
