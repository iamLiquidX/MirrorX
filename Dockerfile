Use Official Python Image
FROM python:slim

WORKDIR /

ENV LD_LIBRARY_PATH /usr/local/lib

# Deps
RUN sed -i 's/main/main non-free/g' /etc/apt/sources.list && \
    apt-get -qq update && \
    apt-get -qq install -y \
                 libcurl4-openssl-dev \
                 libcrypto++-dev libsqlite3-dev libc-ares-dev \
		 libfreeimage-dev \
                 libsodium-dev \
                 libssl-dev \
                 libmagic-dev && \
    apt-get install -y tzdata curl aria2 p7zip-full p7zip-rar wget xz-utils && \
    apt-get -y autoremove && rm -rf /var/lib/apt/lists/* && apt-get clean && \
    wget -q https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-amd64-static.tar.xz && \
    tar -xf ff*.tar.xz && rm -rf *.tar.xz && \
    mv ff*/ff* /usr/local/bin/ && rm -rf ff*

# Home Dir
WORKDIR /app/

# Mirror Bot files and requirements
COPY . .
RUN mv extract /usr/local/bin && \
    mv pextract /usr/local/bin && \
    chmod +x /usr/local/bin/extract && \
    chmod +x /usr/local/bin/pextract && \
    wget -q https://github.com/P3TERX/aria2.conf/raw/master/dht.dat -O /app/dht.dat && \
    wget -q https://github.com/P3TERX/aria2.conf/raw/master/dht6.dat -O /app/dht6.dat && \
    mkdir -p /root/ && \
    mv netrc /root/.netrc && \
    pip3 -q install --no-cache-dir -r requirements.txt

# Script Which Starts the Bot
CMD ["bash", "start.sh"]
