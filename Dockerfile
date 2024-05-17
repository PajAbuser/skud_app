FROM python:3.10

RUN pip install uwsgi

COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app

COPY skud_app .

RUN pip install gunicorn
COPY entrypoint.sh .

ENTRYPOINT [ "./entrypoint.sh" ]
