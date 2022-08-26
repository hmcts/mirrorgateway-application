#!/usr/bin/env bash

python save_env.py > /mirror-gateway-dequeue/env_vars.sh

cron -f &

tail -f /var/log/cron.log
