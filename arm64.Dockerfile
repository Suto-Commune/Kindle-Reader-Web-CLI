# 构建依赖项阶段
FROM python:3.11-slim as builder

WORKDIR /app

COPY requirements.txt .
RUN apt update && \
    apt install -y --no-install-recommends build-essential && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    apt remove -y build-essential && \
    apt autoremove -y && \
    rm -rf /var/lib/apt/lists/*

# 运行时阶段
FROM busybox:latest

ARG READER_VERSION

WORKDIR /reader

RUN wget -O jre.tar.gz https://github.com/adoptium/temurin19-binaries/releases/download/jdk-19.0.2%2B7/OpenJDK19U-jre_aarch64_linux_hotspot_19.0.2_7.tar.gz && \
    tar -zxvf jre.tar.gz && \
    rm -rf jre.tar.gz && \
    wget -O - https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.32-r0/glibc-2.32-r0.apk | tar xz && \
    wget -O - https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.32-r0/glibc-bin-2.32-r0.apk | tar xz && \
    wget -O - https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.32-r0/glibc-i18n-2.32-r0.apk | tar xz && \
    /usr/glibc-compat/bin/localedef -i en_US -f UTF-8 en_US.UTF-8 && \
    ln -s /usr/glibc-compat/lib/ld-linux-aarch64.so.1 /lib/ld-linux-aarch64.so.1 && \
    wget -O reader-pro.jar https://reader-download.fucktx.eu.org/reader-pro-${READER_VERSION}.jar && \
    rm -rf /var/cache/apk/* /tmp/* /var/tmp/* && \
    chmod +x reader-pro.jar

COPY --from=builder /usr/local/ /usr/local/

COPY nginx/conf /etc/nginx/
COPY start.sh .

EXPOSE 1000 5000 8080

ENTRYPOINT ["/bin/sh", "-c", "/reader/start.sh"]
