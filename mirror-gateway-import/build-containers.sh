
docker build -t makeaplea_mgw mirror_gateway
docker build -t makeaplea_mgw_dequeue message_consumer
docker build -t makeaplea_mgw_import .

docker tag makeaplea_mgw registry.service.dsd.io/makeaplea_mgw:latest
docker tag makeaplea_mgw_dequeue registry.service.dsd.io/makeaplea_mgw_dequeue:latest
docker tag makeaplea_mgw_import registry.service.dsd.io/makeaplea_mgw_import:latest
