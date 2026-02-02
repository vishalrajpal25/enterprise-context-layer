-- Seed vector store with placeholder embeddings (deterministic for tests)
-- In production, use real embeddings (e.g. sentence-transformers). For local/demo we use fixed vectors so semantic search returns known results.
-- pgvector: build vector(384) from repeated float.

INSERT INTO embeddings (id, type, content_text, embedding, metadata)
SELECT 'vec_g_001', 'glossary_term', 'Revenue: Income generated from normal business operations. Synonyms: income, sales.',
  ('[' || array_to_string(array_agg(0.1::float), ',') || ']')::vector(384), '{"asset_registry_id": "ar_g_001", "term": "revenue", "domain": "finance"}'::jsonb
FROM generate_series(1, 384) _
ON CONFLICT (id) DO UPDATE SET content_text = EXCLUDED.content_text, embedding = EXCLUDED.embedding, metadata = EXCLUDED.metadata;

INSERT INTO embeddings (id, type, content_text, embedding, metadata)
SELECT 'vec_g_002', 'glossary_term', 'APAC Asia-Pacific region for finance reporting. Countries: JP KR SG HK TW AU NZ IN CN.',
  ('[' || array_to_string(array_agg(0.2::float), ',') || ']')::vector(384), '{"asset_registry_id": "ar_g_002", "term": "APAC", "domain": "reference"}'::jsonb
FROM generate_series(1, 384) _
ON CONFLICT (id) DO UPDATE SET content_text = EXCLUDED.content_text, embedding = EXCLUDED.embedding, metadata = EXCLUDED.metadata;

INSERT INTO embeddings (id, type, content_text, embedding, metadata)
SELECT 'vec_g_003', 'glossary_term', 'Net Revenue: Recognized revenue per ASC 606 minus refunds.',
  ('[' || array_to_string(array_agg(0.15::float), ',') || ']')::vector(384), '{"asset_registry_id": "ar_g_003", "term": "net_revenue", "domain": "finance"}'::jsonb
FROM generate_series(1, 384) _
ON CONFLICT (id) DO UPDATE SET content_text = EXCLUDED.content_text, embedding = EXCLUDED.embedding, metadata = EXCLUDED.metadata;

INSERT INTO embeddings (id, type, content_text, embedding, metadata)
SELECT 'vec_tk_001', 'tribal_knowledge', 'Q4 2019 APAC data incomplete. Oracle to Snowflake migration. Revenue underreported ~15%.',
  ('[' || array_to_string(array_agg(0.12::float), ',') || ']')::vector(384), '{"asset_registry_id": "ar_tk_001", "scope_tables": ["finance.fact_revenue_daily"], "scope_dimensions": ["region=APAC", "period=2019-Q4"]}'::jsonb
FROM generate_series(1, 384) _
ON CONFLICT (id) DO UPDATE SET content_text = EXCLUDED.content_text, embedding = EXCLUDED.embedding, metadata = EXCLUDED.metadata;
