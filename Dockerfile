FROM python:3.11-alpine

ARG READER_VERSION

WORKDIR /reader

COPY --chmod=755 . .

RUN apk add --no-cache \
        nginx \
        git \
        tzdata \
        bash && \
    pip install --upgrade pip && \
    wget https://github.com/adoptium/temurin19-binaries/releases/download/jdk-19.0.1%2B10/OpenJDK19U-jre_x64_alpine-linux_hotspot_19.0.1_10.tar.gz -O jre.tar.gz && \
    tar -zxvf jre.tar.gz && \
    pip install -r requirements.txt && \
    if [ "${READER_VERSION}" = "2.7.4" ]; \
    then rm -rf reader-pro.jar && wget https://reader-download.fucktx.eu.org/reader-pro-2.7.4.jar -O reader-pro.jar; fi && \
    rm -rf \
        /reader/jre.tar.gz \
        /tmp/* \
        /root/.cache \
        /var/cache/apk/* \
        /etc/nginx/*

COPY --chmod=755 ./nginx/conf /etc/nginx/

ENTRYPOINT [ "/reader/start.sh" ]

EXPOSE 1000 5000 8080