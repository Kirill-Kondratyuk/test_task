FROM python:3.6-alpine3.8

ENV PYTHONUNBUFFERED=1

RUN apk add sqlite

WORKDIR /wd

COPY generator.py .
COPY parser.py .
COPY main.py .
COPY models.py .
COPY dict.txt .
COPY requirements.txt .
COPY entrypoint.sh .

RUN chmod +x generator.py
RUN chmod +x main.py
RUN chmod +x models.py
RUN chmod +x entrypoint.sh

RUN pip install -r requirements.txt

ENTRYPOINT ["sh", "entrypoint.sh"]