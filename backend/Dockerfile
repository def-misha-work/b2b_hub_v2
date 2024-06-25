FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN apt-get update && apt-get install -y python3-pip
RUN apt-get install -y libpq-dev python-dev-is-python3
RUN pip3 install -r requirements.txt
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "b2b_hub.wsgi"]
