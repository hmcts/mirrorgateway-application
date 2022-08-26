#!/usr/bin/env bash

cd /mirror-gateway-import

python ./save_env.py > ./env_vars.sh

cron -f &

tail -f /var/log/cron.log
