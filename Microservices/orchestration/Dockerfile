FROM alpine:3.7
RUN apk update
RUN apk add python3
RUN apk add py3-pip
RUN pip3 install Flask 
RUN pip3 install -U flask-cors
RUN pip3 install requests

WORKDIR /app
COPY . /app
EXPOSE 5000
ENV TEAM_ID CC_096_101_120_121
CMD ["python3", "server.py"]

