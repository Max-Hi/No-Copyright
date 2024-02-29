FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

ENV FLASK_APP=api/__init__.py
ENV FLASK_DEBUG=1

CMD ["flask", "run", "--host=0.0.0.0"]
