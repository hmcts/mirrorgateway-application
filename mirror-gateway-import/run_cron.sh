#!/usr/bin/env bash

cd /makeaplea_dx

python ./save_env.py > ./env_vars.sh

cron -f &

tail -f /var/log/cron.log
