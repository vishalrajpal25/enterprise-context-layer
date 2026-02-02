-- Asset Registry (PostgreSQL) - ECP Context Registry
-- Run against ecp_registry database

CREATE TABLE IF NOT EXISTS assets (
    id VARCHAR(50) PRIMARY KEY,
    type VARCHAR(50) NOT NULL,
    version INT NOT NULL DEFAULT 1,
    content JSONB NOT NULL,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    created_by VARCHAR(100),
    updated_by VARCHAR(100)
);

CREATE INDEX IF NOT EXISTS idx_assets_type ON assets(type);
CREATE INDEX IF NOT EXISTS idx_assets_content ON assets USING GIN(content);
CREATE INDEX IF NOT EXISTS idx_assets_metadata ON assets USING GIN(metadata);
