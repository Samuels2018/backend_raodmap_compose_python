FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN python -venv .venv
RUN .venv/bin/activate
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


CMD ["python", "manage.py", "runserver", ]