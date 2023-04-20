FROM python:3.9-slim

RUN apt-get -y update
RUN apt-get -y install git make

ENV PIP_NO_CACHE_DIR=yes \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /home/app

# Copy the requirements.txt file and install the requirements
COPY requirements.txt .
RUN sed -i '/Items below this point will not be included in the Docker Image/,$d' requirements.txt && \
	pip install --no-cache-dir -r requirements.txt

COPY .env ./
COPY . .

CMD ["make", "run_api"]
