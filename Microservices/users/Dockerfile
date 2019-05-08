FROM alpine:3.7
RUN apk update
RUN apk add python
RUN apk add py-pip
RUN pip install Flask 
RUN pip install -U flask-cors

WORKDIR /app
COPY . /app
EXPOSE 80
ENV TEAM_ID CC_096_101_120_121
CMD ["python", "app.py"]

