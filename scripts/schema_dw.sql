-- Synthetic data warehouse (ecp_dw) for Cube - fake fact/dim tables

CREATE TABLE IF NOT EXISTS dim_region (
    region_code VARCHAR(10) PRIMARY KEY,
    region_name VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS fact_revenue_daily (
    id SERIAL PRIMARY KEY,
    transaction_date DATE NOT NULL,
    region_code VARCHAR(10) NOT NULL REFERENCES dim_region(region_code),
    fiscal_period VARCHAR(10) NOT NULL,
    amount NUMERIC(18,2) NOT NULL,
    type VARCHAR(20) NOT NULL
);

INSERT INTO dim_region (region_code, region_name) VALUES
('APAC', 'Asia-Pacific'),
('EMEA', 'Europe Middle East Africa'),
('NA', 'North America')
ON CONFLICT (region_code) DO NOTHING;

-- Synthetic rows: APAC revenue for Q3 2024 (Oct-Dec 2024) and one budget row
INSERT INTO fact_revenue_daily (transaction_date, region_code, fiscal_period, amount, type) VALUES
('2024-10-01', 'APAC', 'Q3-2024', 45000000, 'recognized'),
('2024-11-01', 'APAC', 'Q3-2024', 48000000, 'recognized'),
('2024-12-01', 'APAC', 'Q3-2024', 49300000, 'recognized'),
('2024-10-01', 'APAC', 'Q3-2024', 135000000, 'budget')
ON CONFLICT DO NOTHING;
