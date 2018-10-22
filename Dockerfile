FROM python:3.7-stretch

WORKDIR /app

RUN \
       apt-get update \
    && apt-get upgrade -y

RUN pip3.7 install --upgrade pip

COPY requirements.txt .
RUN pip3.7 install --upgrade -r requirements.txt

COPY src src
COPY main.py .

ENTRYPOINT [ "python3.7", "main.py" ]
CMD []