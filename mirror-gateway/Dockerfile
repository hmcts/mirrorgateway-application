FROM jboss/wildfly:8.2.1.Final 

ENV JAVA_OPTS="-Xss256k -Xms768m -Xmx768m -Xmn256m -XX:SurvivorRatio=4 -XX:-UseAdaptiveSizePolicy -XX:+UseParNewGC -Djava.net.preferIPv4Stack=true"

COPY ddl /opt/jboss/ddl
COPY setup_db.sh /opt/jboss/
USER root
RUN yum install -y postgresql-contrib
RUN yum install -y postgresql
RUN chmod +x setup_db.sh
USER jboss

COPY mirrorgateway.properties /opt/jboss/wildfly/standalone/configuration/
COPY postgres-driver/postgresql-9.4-1203.jdbc4.jar /opt/jboss/wildfly/standalone/deployments/
COPY map_mgw.war /opt/jboss/
COPY configure.sh /opt/jboss/
COPY run.sh /opt/jboss/
COPY delete_old_data.sh /opt/jboss/

COPY cgi-soap-gateway/map_mgw.war /opt/jboss/

CMD ["/bin/bash", "run.sh"]
