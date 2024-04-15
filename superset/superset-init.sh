#!/bin/bash

echo "Creating admin user: ${SUPERSET_ADMIN_USER} (${SUPERSET_ADMIN_EMAIL})..."
superset fab create-admin \
  --username "$SUPERSET_ADMIN_USER" \
  --firstname Superset --lastname Admin \
  --email "$SUPERSET_ADMIN_EMAIL" \
  --password "$SUPERSET_ADMIN_PASSWORD"

echo "Upgrading DB..."
superset db upgrade

echo "Initializing Superset..."
superset superset init

echo "Starting server..."
/bin/sh -c /usr/bin/run-server.sh