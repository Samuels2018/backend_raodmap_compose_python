#!/bin/bash
set -e

# Crear usuario de aplicación
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
  CREATE USER "${APP_USER}" WITH PASSWORD '${APP_PASSWORD}';
EOSQL

# Crear cada base de datos y asignar privilegios
for db in $(echo ${APP_DATABASES} | tr ',' ' '); do
  psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE DATABASE "${db}";
    GRANT ALL PRIVILEGES ON DATABASE "${db}" TO "${APP_USER}";
EOSQL
done