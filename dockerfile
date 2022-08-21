FROM python:3.10-slim-buster
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD python ratestask/app.py