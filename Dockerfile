FROM python:slim

ARG CPU_ARCH="amd64"
ENV HOST_CPU_ARCH=$CPU_ARCH

WORKDIR /
# Deps
RUN sed -i 's/main/main non-free/g' /etc/apt/sources.list && \
    apt-get -qq update && \
    apt-get -qq install -y tzdata curl aria2 p7zip-full p7zip-rar wget xz-utils libmagic-dev && \
    apt-get -y autoremove && rm -rf /var/lib/apt/lists/* && apt-get clean && \
    wget -q https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-${HOST_CPU_ARCH}-static.tar.xz && \
    tar -xf ff*.tar.xz && rm -rf *.tar.xz && \
    mv ff*/ff* /usr/local/bin/ && rm -rf ff* && \
    wget -q https://github.com/viswanathbalusu/megasdkrest/releases/download/v0.1.0/megasdkrest-${HOST_CPU_ARCH} -O /usr/local/bin/megasdkrest && \
    chmod a+x /usr/local/bin/megasdkrest

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
