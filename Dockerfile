

FROM python:3.10-slim-bookworm

RUN pip install --no-cache-dir -r requirements.txt

# Updating Packages

RUN apt-get update && apt-get install -y git curl python3-pip ffmpeg \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copying Requirements
COPY requirements.txt /requirements.txt

# Installing Requirements
RUN cd /
RUN pip3 install --upgrade pip
RUN pip3 install -U -r requirements.txt

# Setting up working directory
RUN mkdir /MusicPlayer
WORKDIR /MusicPlayer

# Preparing for the Startup
COPY startup.sh /startup.sh
RUN chmod +x /startup.sh

# Running Music Player Bot
CMD ["/bin/bash", "/startup.sh"]
