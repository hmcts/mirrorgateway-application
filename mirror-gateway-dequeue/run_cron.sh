#!/usr/bin/env bash

python save_env.py > /MessageConsumer/env_vars.sh

cron -f &

tail -f /var/log/cron.log
