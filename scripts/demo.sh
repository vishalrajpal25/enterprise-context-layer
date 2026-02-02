#!/usr/bin/env bash
# ECP demo script - run against local API with synthetic data.
# Prerequisites: docker compose up, scripts/seed_all.sh, API running on port 8000.

set -e
BASE_URL="${BASE_URL:-http://localhost:8000}"

echo "=== ECP Demo: Resolve and Execute ==="
echo "Base URL: $BASE_URL"
echo ""

echo "1. Resolve: 'APAC revenue last quarter'"
RESOLVE_RESP=$(curl -s -X POST "$BASE_URL/api/v1/resolve" \
  -H "Content-Type: application/json" \
  -d '{"concept": "APAC revenue last quarter", "user_context": {"department": "finance", "role": "analyst"}}')
echo "$RESOLVE_RESP" | python3 -m json.tool 2>/dev/null || echo "$RESOLVE_RESP"

RESOLUTION_ID=$(echo "$RESOLVE_RESP" | python3 -c "import sys, json; print(json.load(sys.stdin).get('resolution_id', ''))" 2>/dev/null || true)
if [ -z "$RESOLUTION_ID" ] || [ "$RESOLUTION_ID" = "None" ]; then
  echo "No resolution_id; check API and seeds. Skipping execute."
  exit 0
fi

echo ""
echo "2. Execute (resolution_id=$RESOLUTION_ID)"
EXEC_RESP=$(curl -s -X POST "$BASE_URL/api/v1/execute" \
  -H "Content-Type: application/json" \
  -d "{\"resolution_id\": \"$RESOLUTION_ID\", \"parameters\": {}}")
echo "$EXEC_RESP" | python3 -m json.tool 2>/dev/null || echo "$EXEC_RESP"

echo ""
echo "3. Glossary: query 'revenue'"
curl -s "$BASE_URL/api/v1/glossary?query=revenue" | python3 -m json.tool 2>/dev/null || true

echo ""
echo "4. Lineage: target 'net_revenue'"
curl -s "$BASE_URL/api/v1/lineage?target=net_revenue" | python3 -m json.tool 2>/dev/null || true

echo ""
echo "5. Metrics: dimension 'region'"
curl -s "$BASE_URL/api/v1/metrics?dimension=region" | python3 -m json.tool 2>/dev/null || true

echo ""
echo "=== Demo complete ==="
