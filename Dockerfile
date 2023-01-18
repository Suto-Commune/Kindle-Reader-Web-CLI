FROM eclipse-temurin:19-jre-alpine
FROM python:alpine
WORKDIR /reader
EXPOSE 5000
EXPOSE 8080
COPY requirements.txt .
RUN chmod +x requirements.txt
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
COPY . .
CMD [ "python","main.py" ]