#!/bin/bash

export PGPASSWORD=$DB_PASSWORD

function ts {
  date -Iseconds -u
}

echo "$(ts) Blanking out old audit messages"
psql -h $DB_HOST -U $DB_USERNAME -d pleaonline -c "UPDATE message_audit SET message_content='' WHERE updated_date < NOW() - interval '30 days';"

echo "$(ts) ALL DONE"
