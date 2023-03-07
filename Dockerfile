FROM python:alpine

WORKDIR /reader

COPY --chmod=755 . .

RUN apk add --no-cache \
        nginx \
        git \
        tzdata \
        bash && \
    apk add --no-cache --virtual=build-dependencies \
        gcc \
        libc-dev \
        libffi-dev \
        build-base \
        musl-dev \
        make && \
    if [ "$(uname -m)" = "x86_64" ]; then \
        wget https://github.com/adoptium/temurin19-binaries/releases/download/jdk-19.0.1%2B10/OpenJDK19U-jre_x64_alpine-linux_hotspot_19.0.1_10.tar.gz -O jre.tar.gz && \
        tar -zxvf jre.tar.gz; \
    elif [ "$(uname -m)" = "aarch64" ]; then \
        wget https://github.com/adoptium/temurin19-binaries/releases/download/jdk-19.0.2%2B7/OpenJDK19U-jre_aarch64_linux_hotspot_19.0.2_7.tar.gz -O jre.tar.gz && \
        tar -zxvf jre.tar.gz && \
        cd /reader/docker/arm64/whl && \
        bash install_whl.sh; \
    fi && \
    pip install -r requirements.txt && \
    apk del --purge \
        build-dependencies && \
    rm -rf \
        /reader/jre.tar.gz \
        /tmp/* \
        /root/.cache \
        /var/cache/apk/*

COPY --chmod=755 ./nginx/conf /etc/nginx/

ENTRYPOINT [ "/reader/start.sh" ]

EXPOSE 1000 5000 8080