-- pgvector schema for semantic index (ecp_vectors database)
-- Embeddings for glossary and tribal knowledge

CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS embeddings (
    id VARCHAR(100) PRIMARY KEY,
    type VARCHAR(50) NOT NULL,
    content_text TEXT,
    embedding vector(384),
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_embeddings_type ON embeddings(type);
CREATE INDEX IF NOT EXISTS idx_embeddings_metadata ON embeddings USING GIN(metadata);
-- Vector similarity index (use ivfflat or hnsw depending on pgvector version)
CREATE INDEX IF NOT EXISTS idx_embeddings_vector ON embeddings USING hnsw (embedding vector_cosine_ops);
