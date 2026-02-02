#!/bin/bash
set -e
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
  CREATE DATABASE ecp_vectors;
  CREATE DATABASE ecp_dw;
EOSQL
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname ecp_vectors <<-EOSQL
  CREATE EXTENSION IF NOT EXISTS vector;
EOSQL
