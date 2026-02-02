#!/usr/bin/env bash
# Run all seeds (requires docker compose up and DBs initialized).
# Usage: ./scripts/seed_all.sh
# Or: PGHOST=localhost PGUSER=ecp PGPASSWORD=changeme ./scripts/seed_all.sh

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

PGHOST="${PGHOST:-localhost}"
PGPORT="${PGPORT:-5432}"
PGUSER="${PGUSER:-ecp}"
PGPASSWORD="${PGPASSWORD:-changeme}"
export PGPASSWORD

echo "Seeding Asset Registry (ecp_registry)..."
psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d ecp_registry -f scripts/schema_registry.sql
psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d ecp_registry -f scripts/seed_registry.sql

echo "Seeding Vector store (ecp_vectors)..."
psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d ecp_vectors -f scripts/schema_vectors.sql
psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d ecp_vectors -f scripts/seed_vectors.sql

echo "Seeding Synthetic DW (ecp_dw)..."
psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d ecp_dw -f scripts/schema_dw.sql

echo "Neo4j: run scripts/seed_neo4j.cypher manually via Neo4j Browser or cypher-shell."
echo "  Example: docker exec -i ecp-neo4j cypher-shell -u neo4j -p changeme < scripts/seed_neo4j.cypher"
echo "Seeds done."
