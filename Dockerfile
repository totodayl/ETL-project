FROM python:3.10
LABEL authors="eroma"


RUN apt-get update && apt-get install -y wget unzip && \
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb && \
    apt-get clean

WORKDIR /app

COPY op-gg-stats.py /app
COPY s3_upload.py /app
COPY ml-stats.py /app
COPY requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

ENV AWS_ACCESS_KEY_ID_FILE=/run/secrets/aws_access_key_id
ENV AWS_SECRET_ACCESS_KEY_FILE=/run/secrets/aws_secret_access_key

CMD ["python", "op-gg-stats.py"]

