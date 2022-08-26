#!/bin/bash

JBOSS_HOME=/opt/jboss/wildfly
JBOSS_CLI=$JBOSS_HOME/bin/jboss-cli.sh
JBOSS_MODE=${1:-"standalone"}
JBOSS_CONFIG=${2:-"$JBOSS_MODE-full.xml"}

function wait_for_server() {
  until `$JBOSS_CLI -c "ls /deployment" &> /dev/null`; do
    sleep 1
  done
}

echo "=> Starting WildFly server"
$JBOSS_HOME/bin/$JBOSS_MODE.sh -c $JBOSS_CONFIG >/dev/null &

echo "=> Waiting for the server to boot"
wait_for_server

echo "=> Executing the commands"
$JBOSS_CLI --connect <<EOF

# Batch script to add the configuration to the WildFly server
#
# Usage: jboss-cli.sh --file=map_config.cli

# Connect to the running WildFly server
connect 127.0.0.1

# Start batching commands
batch

# Configure system property
/system-property=mirrorgatewayProperties:add(value=\${jboss.server.config.dir}/mirrorgateway.properties)

# Configure the JMS queues
jms-queue add --queue-address=GatewayInboundQueue --entries=java:jboss/GatewayInboundQueue,java:jboss/exported/jboss/GatewayInboundQueue --durable=true
jms-queue add --queue-address=GatewayOutboundQueue --entries=java:jboss/GatewayOutboundQueue,java:jboss/exported/jboss/GatewayOutboundQueue --durable=true

# Configure the JMS Datasource

data-source add --name=MirrorGatewayDS --jndi-name=java:/jdbc/MirrorGatewayDS --driver-name=postgres-driver/postgresql-9.4-1203.jdbc4.jar --driver-class=org.postgresql.Driver --connection-url=jdbc:postgresql://$DB_HOST:$DB_PORT/$DB_NAME --min-pool-size=5 --max-pool-size=10 --user-name=$DB_USERNAME --password=$DB_PASSWORD

# Configure the server log
/subsystem=logging/periodic-rotating-file-handler=FILE:remove
/subsystem=logging/size-rotating-file-handler=FILE:add(level="ALL",file={"path"=>"server.log","relative-to"=>"jboss.server.log.dir"},rotate-size="10m",max-backup-index="50",append=true,autoflush=true)

# Run the batch commands
run-batch

# Reload the server configuration
:reload 

EOF


echo "=> Shutting down WildFly"
if [ "$JBOSS_MODE" = "standalone" ]; then
  $JBOSS_CLI -c ":shutdown"
else
  $JBOSS_CLI -c "/host=*:shutdown"
fi
