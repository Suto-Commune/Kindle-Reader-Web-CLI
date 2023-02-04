FROM python:alpine

RUN apk add nginx
COPY ./nginx/conf /etc/nginx/

WORKDIR /reader

RUN apk add git
RUN wget https://github.com/adoptium/temurin19-binaries/releases/download/jdk-19.0.1%2B10/OpenJDK19U-jre_x64_alpine-linux_hotspot_19.0.1_10.tar.gz -O jre.tar.gz
RUN tar -zxvf jre.tar.gz
RUN rm jre.tar.gz



EXPOSE 1000
EXPOSE 5000
EXPOSE 8080
COPY requirements.txt .
RUN chmod +x requirements.txt
RUN pip install -r requirements.txt
COPY . .

CMD ["sh","start.sh" ]