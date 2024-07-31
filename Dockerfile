FROM python:3.11

COPY . /app
WORKDIR /app

RUN apt-get update && apt-get install nmap

RUN pip install python3-nmap==1.6.0

ENV TZ Asia/Seoul
ENV PYTHONPATH /app

CMD ["python", "main.py"]