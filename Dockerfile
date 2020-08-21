FROM python:3.7.7-buster

RUN apt-get update
RUN mkdir /app

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ARG arg_uid
ARG arg_pwd

ENV sql_uid ${arg_uid}
ENV sql_pwd ${arg_pwd}

ENTRYPOINT ["python"]
CMD ["app.py"]