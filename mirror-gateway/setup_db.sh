#!/usr/bin/env bash

# Run this script to set up the mirrorgateway database

export PGPASSWORD=$DB_PASSWORD

psql -h $DB_HOST -U $DB_USERNAME $DB_NAME < ddl/install.sql
