#!/bin/bash

cd /mirror-gateway-import

source env_vars.sh

python3 -W ignore data_import.py
