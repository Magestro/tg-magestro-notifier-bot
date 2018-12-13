FROM python:3.7-stretch

WORKDIR /app

RUN \
       apt-get update \
    && apt-get upgrade -y \
    && apt-get install git

RUN pip3.7 install --upgrade pip

RUN git clone https://github.com/Magestro/tg-magestro-notifier-bot.git . \
    && git checkout master

RUN pip3.7 install --upgrade -r requirements.txt

ENTRYPOINT [ "python3.7", "main.py" ]
CMD []