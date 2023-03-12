FROM python:3.11-slim

ARG READER_VERSION

WORKDIR /reader

COPY --chmod=755 . .

RUN apt update -y && \
    DEBIAN_FRONTEND=noninteractive apt install -y \
        nginx \
        git \
        tzdata \
        bash \
        wget \
        procps && \
    pip install --upgrade pip && \
    wget https://github.com/adoptium/temurin19-binaries/releases/download/jdk-19.0.2%2B7/OpenJDK19U-jre_aarch64_linux_hotspot_19.0.2_7.tar.gz -O jre.tar.gz && \
    tar -zxvf jre.tar.gz && \
    pip install -r requirements.txt && \
    if [ "${READER_VERSION}" = "2.7.4" ]; \
    then rm -rf reader-pro.jar && wget https://reader-download.fucktx.eu.org/reader-pro-2.7.4.jar -O reader-pro.jar; fi && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf \
        /reader/jre.tar.gz \
	    /tmp/* \
        /root/.cache \
	    /var/lib/apt/lists/* \
	    /var/tmp/* \
        /etc/nginx/*

COPY --chmod=755 ./nginx/conf /etc/nginx/

ENTRYPOINT [ "/reader/start.sh" ]

EXPOSE 1000 5000 8080