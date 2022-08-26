ARG PLATFORM=""
#FROM hmctspublic.azurecr.io/base/java${PLATFORM}:17-distroless
FROM java:8

ENV JAVA_OPTS="-Xss256k -Xms768m -Xmx768m -Xmn256m -XX:SurvivorRatio=4 -XX:-UseAdaptiveSizePolicy -XX:+UseParNewGC -Djava.net.preferIPv4Stack=true"

ENV WILDFLY_VERSION 8.2.1.Final
ENV JBOSS_HOME /opt/jboss/wildfly

# copy mirror-gateway

COPY mirror-gateway/wildfly/wildfly-$WILDFLY_VERSION.tar.gz $JBOSS_HOME

RUN tar xf $JBOSS_HOME/wildfly-$WILDFLY_VERSION.tar.gz \
    && rm $JBOSS_HOME/wildfly-$WILDFLY_VERSION.tar.gz \
    && chown -R jboss:0 ${JBOSS_HOME} \
    && chmod -R g+rw ${JBOSS_HOME}

COPY mirror-gateway/ddl /opt/jboss/ddl
COPY mirror-gateway/setup_db.sh /opt/jboss/
USER root
RUN apt-get install -y postgresql-contrib postgresql
RUN chmod +x setup_db.sh
USER jboss

COPY mirror-gateway/mirrorgateway.properties /opt/jboss/wildfly/standalone/configuration/
COPY mirror-gateway/postgres-driver/postgresql-9.4-1203.jdbc4.jar /opt/jboss/wildfly/standalone/deployments/
COPY mirror-gateway/cgi-soap-gateway/map_mgw.war /opt/jboss/
COPY mirror-gateway/configure.sh /opt/jboss/
COPY mirror-gateway/run.sh /opt/jboss/
COPY mirror-gateway/delete_old_data.sh /opt/jboss/


# copy mirror-gateway-dequeue

WORKDIR /mirror-gateway-dequeue
COPY ./mirror-gateway-dequeue/* $WORKDIR

RUN apt-get update \
    && apt-get install -y cron
RUN crontab cron.conf \
    && touch /var/log/cron.log \
    && $WORKDIR/run_cron.sh &


# copy mirror-gateway-import

WORKDIR /mirror-gateway-import
RUN apt-get install -y build-essential python3.6 python3-pip python3.6-venv gnupg
COPY mirror-gateway-import/* $WORKDIR
RUN pip install --no-cache-dir -r $WORKDIR/requirements.txt
RUN gpg --import $WORKDIR/gpg-public-key/sustainingteamsupport-public-key.gpg

RUN crontab ./cron.conf \
    && touch /var/log/cron.log \
    && $WORKDIR/run_cron.sh &


CMD ["/bin/bash", "/opt/jboss/run.sh"]