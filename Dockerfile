FROM python:3.10
LABEL authors="eroma"

# Install dependencies
RUN apt-get update && apt-get install -y wget unzip && \
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb && \
    apt-get clean

# Set up the application directory
WORKDIR /app
run
# Copy application files
COPY op-gg-stats.py /app
COPY s3_upload.py /app
COPY ml-stats.py /app
COPY requirements.txt /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables for AWS credentials
ENV AWS_ACCESS_KEY_ID_FILE=/run/secrets/aws_access_key_id
ENV AWS_SECRET_ACCESS_KEY_FILE=/run/secrets/aws_secret_access_key

# Use /tmp directory for temporary files
ENV TMPDIR=/tmp

# Command to run the application
CMD ["python", "op-gg-stats.py"]


