FROM java:8

VOLUME ["/data"]

RUN apt-get update
RUN apt-get -y install cron

ENV WORKDIR=/MessageConsumer
COPY . $WORKDIR
WORKDIR $WORKDIR

RUN apt-get install cron
RUN crontab cron.conf
RUN touch /var/log/cron.log

CMD ["/bin/bash", "run_cron.sh"]
