#!/bin/bash

cd /mirror-gateway-dequeue

source env_vars.sh

./MessageConsumer.sh $WILDFLY_APPLICATION_USER $WILDFLY_APPLICATION_PASS jboss/GatewayInboundQueue http-remoting://${MGW_HOST:-127.0.0.1\:8080} /data
