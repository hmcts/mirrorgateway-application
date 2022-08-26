FROM python:3.6

RUN apt-get update && apt-get install -y gnupg cron \
      && rm -rf /var/lib/apt/lists/*

WORKDIR /makeaplea_dx

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN gpg --import ./gpg-public-key/sustainingteamsupport-public-key.gpg

VOLUME ["/data"]
VOLUME ["/archive"]
VOLUME ["/logs"]

RUN crontab ./cron.conf
RUN touch /var/log/cron.log

CMD ["/bin/bash", "./run_cron.sh"]

