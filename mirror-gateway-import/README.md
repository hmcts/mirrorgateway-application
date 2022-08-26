makeaplea_dx
============

Overview
--------

This repo holds the configuration to build the docker images that run on the MaP Mirror gateway. The mirror gateway receives court case and resulting data from Libra via CGI's soap gateway system.  The mirror gateway is the makea-a-plea hosted element of CGI's soap gateway solution.

Associated configuration exists in the makeaplea-deploy repository for provisioning staging (template-deploy environment: staging-mgw) and production (template-deploy environment: prod-mgw) stacks.  

The mirror gateway instance runs 3 docker containers: the mirror gateway container, the dequeuing container and the import container.  

### Mirror gateway container

Dockerfile: mirror_gateway/Dockerfile

This runs a Java Wildfly application server which runs the mirror gateway war file, as provided by CGI.  The mirror gateway presents a SOAP API endpoint and decrypts incoming data. The data is then stored in a database, which is seperate to the MaP database.

The database schema is available in the ``/mirror_gateway/ddl`` directory.

### The dequeing container

    Dockerfile: message_consumer/Dockerfile

This container runs a java file (which was provided by CGI) at 2am each day. The application queries the mirror gateway instance and saves the XML to the local file system.  Note, the container is configured to MaP the data directory to the host instances file system.

The ``dequeue_messages.sh`` script can be run at anytime to retrieve messages from the soap gateway for example in the prod-mgw environment you coudl run:

NOTE: Wildfly provides an admin interface and a cli tool.  The cli tool seems to be lacking in features which has resulted in a slightly convoluted Docker build process.  The Dockerfile builds the application, then a run.sh script does initial user creation on the first time the container is instantiated.

NOTE: The version of Wildly has been specified by CGI based on testing they have performed with their mirror gateway software. Any version changes would need to be done in collaboration with CGI.

    docker exec makeaplea_mgw_dequeue ./dequeue_messages.sh

This will retrieve all new data from the mirror gateway instance and write it to disc.  The current configuration stores data files in /var/mgw-data on the host instance.

### The import container

    Dockerfile: ./Dockerfile

This container runs a python script each night [see: ``./docker/cron.conf``]. The container iterates over all files imported by the dequeuing container, validates each file against an XSD, and then attempts to import each element (case or result) into MaP via MaP's REST interface.

The import can be run manually on an instance with the following command:

``docker exec makeaplea_mgw_import ./data_import.py``

The import script produces a status email [NOTE: recipients are managed in the makeaplea-deploy respository]

### Build process

Unlike the rest of the MaP application the mirror gateway is currently not managed by Jenkins, due to changes needing to be being made very infrequently.

Therefore if changes need to be made to an image then the image will need to be rebuilt on a developer's local machine and pushed into the MOJD docker repository. Once that has been done, then the relevant environment (makeaplea-deploy: staging-mgw or prod-mgw), can be highstated to pull the latest docker image to the instance and recreate the relevant container.

The steps to build, tag and push a docker image are outlined in the ``./build-containers.sh`` file. The credentials for the MOJD docker registry are in the relevant environment's pillar in the makeaplea-deploy repository.

Local development environment
-----------------------------

You can provision a local development environment using docker-compose.

From the makeaplea_dx root directory run the following commands:

#### To build all containers:
    docker-compose build

#### To run all containers:
    docker-compose up

#### Viewing the wildly holding page in the browser navigate to:
    {dockerIP}:8080

#### Accessing the wildfly admin console in the brower:
    {dockerIP}:9990

NOTE: authentication details are in the docker-compose.yaml file.

NOTE: Whilst the admin console is available on the production and staging wildfly instances if required, port 9990 is not open and it is preferable to make changes to the docker build process rather than using the widfly admin interface.

#### To create the mirror gateway schema:
    docker-compose run mgw ./setup_db.sh

#### To run the dequeing job:
    docker-compose mgw_dequeue ./dequeue_messages.sh

#### To run the import job:
    docker-compose mgw_import ./data-import.py

NOTE: If required, you can tweak the environment variables in the ``docker-compose.yaml`` file to point the import script at a local dev instance of MaP.

Manually running the import on staging or production
----------------------------------------------------

Log into the instance

### Dequeue the messages

    docker exec makeaplea_mgw_dequeue ./dequeue_messages.sh

This will be downloaded messages into ``/var/mgw-data/`` on the host instance.

### Import the messages

    docker exec makeaplea_mgw_import ./data_import.py

This process may take a long time to complete, depending on the amount of data that needs to be imported.

Checking the status of the production instance
----------------------------------------------

If CGI have issues sending data to the soap gateway they will ask you to check the status of the server.

The following checks are useful:

1. can you view the wildfly holding page in a web browser (requires VPN access) ``https://libra-dx.makeaplea.justice.gov.uk`` and can you access the WSDL?  ``https://libra-dx.makeaplea.justice.gov.uk/map_mgw/service/mapmirrorgatewayapi/?wsdl``?

NOTE: The certificate is self signed but "trusted" by CGI's SOAP gateway software, so it will produce an error in the browser but is still valid.

2. Do the mirror gateway container logs show anything unusual (exceptions, warnings, etc.): ``docker logs makeaplea_mgw``

3. Does the dequeing script run without errors?  This communicates with the Wildfly appplication server and thus is a good test that the gateway is running ``docker exec makeaplea_mgw_dequeue ./dequeue_messages.sh``

4. The import script tars and gpg encrypts the files that were processed and stores them in the ``/var/mgw-archive`` directory on the host/instance. Checking this directory will tell you when the script last processed data.

Monitoring
----------

The MOJD platforms team have monitor the production mirror gateway instance raising an alert if they don't receive log data from the import container every 24 hours.