#!/bin/bash

grep $WILDFLY_MANAGEMENT_USER ./wildfly/standalone/configuration/mgmt-users.properties

if [[ $? -ne "0" ]];
then
    /bin/bash ./configure.sh standalone standalone-full.xml
    ./wildfly/bin/add-user.sh --silent -u $WILDFLY_MANAGEMENT_USER -p $WILDFLY_MANAGEMENT_PASS -g superuser -e
    ./wildfly/bin/add-user.sh --silent -a -u $WILDFLY_APPLICATION_USER -p $WILDFLY_APPLICATION_PASS -g guest -e
    rm -rf ./wildfly/standalone/configuration/standalone_xml_history/current
    cp map_mgw.war ./wildfly/standalone/deployments/
fi

./wildfly/bin/standalone.sh -c standalone-full.xml -b 0.0.0.0 -bmanagement 0.0.0.0
