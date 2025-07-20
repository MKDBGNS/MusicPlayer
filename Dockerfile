FROM python:3.10-slim-bookworm

RUN apt-get update && apt-get install -y git curl python3-pip ffmpeg \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python3", "main.py"]
