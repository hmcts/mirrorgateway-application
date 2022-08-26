#! /bin/sh
#
# Usage:
# MessageConsumer.sh <username> <password> <queue> <providerURL> <baseDir>
#
# username:       Username of the WildFly user who can consume JMS messages
# password:       Password of the WildFly user who can consume JMS messages
# queue:          JNDI name of the WildFly JMS queue to consume messages from
# providerURL:    Provider URL for the WildFly JNDI remote lookup
# baseDir:        Directory in which to create the sub-folder for writing the JMS messages into
#
# Example:
# MessageConsumer.sh appuser password jboss/GatewayInboundQueue http-remoting://127.0.0.1:8080 /var/map
#

# Configure java home directory
JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/

# Configure parameters
username=$1
password=$2
queue=$3
senderId="MAP_MGW"
providerURL=$4
baseDir=$5
runDate=`date +%Y%m%d`

# Example call to jar
# java -jar cgi-soap-gateway/WFMessageConsumer.jar <username> <password> <queue> <senderId> <providerURL> <baseDir> <runDate>
# java -jar cgi-soap-gateway/WFMessageConsumer.jar appuser password jboss/GatewayInboundQueue MAP_MGW http-remoting://127.0.0.1:8080 /var/map 20150925

# Write each JMS message to a file
$JAVA_HOME/bin/java -jar cgi-soap-gateway/WFMessageConsumer.jar $username $password $queue $senderId $providerURL $baseDir $runDate

# Return exit code from jar which will be non-zero if
# an error occurred while processing the JMS messages
exit $?
