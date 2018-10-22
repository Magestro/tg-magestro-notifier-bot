FROM python:3.7-stretch

WORKDIR /app

RUN \
       apt-get update \
    && apt-get upgrade -y \
    && apt-get install git

RUN git clone https://github.com/Magestro/tg-magestro-notifier-bot.git . \
    && git checkout v0.1.0

RUN pip3.7 install --upgrade pip
RUN pip3.7 install --upgrade -r requirements.txt

ENTRYPOINT [ "python3.7", "main.py" ]
CMD []