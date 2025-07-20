FROM python:3.10-slim-bookworm

# 🔧 Updating Packages
RUN apt-get update && apt-get install -y git curl python3-pip ffmpeg \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 📦 Copying Requirements
COPY requirements.txt /requirements.txt

# ✅ 🔥 Force rebuild and bust stream.py cache
RUN rm -rf /app/core/stream.py \
    && echo "stream.py cleared for rebuild" > /dev/null

# 💻 Installing Requirements
RUN cd /
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -U -r requirements.txt

# 🗂️ Setting up working directory
#RUN mkdir /MusicPlayer
#WORKDIR /MusicPlayer



# 🎶 Running Music Player Bot
#CMD ["/bin/bash", "/startup.sh"]
CMD ["python3", "/MusicPlayer/main.py"]
