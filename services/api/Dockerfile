FROM python:3.7-alpine
WORKDIR /usr/src/app


COPY ./ ./
RUN pip3 install -r requirements.txt

CMD ["flask", "run", "--host=0.0.0.0"]