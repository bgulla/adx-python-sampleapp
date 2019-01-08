FROM python:2
MAINTAINER Brandon Gulla "hey@brandongulla.com"

COPY . /app
RUN chown -R 1001:0 /app

WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
EXPOSE 8080

USER 1001
CMD ["app.py"]
