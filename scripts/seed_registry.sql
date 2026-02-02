-- Seed Asset Registry with synthetic finance-domain assets (glossary, tribal knowledge, validation rules)

INSERT INTO assets (id, type, content, metadata) VALUES
('ar_g_001', 'glossary_term', '{
  "canonical_name": "revenue",
  "display_name": "Revenue",
  "definition": "Income generated from normal business operations",
  "variations": [
    {"context": "sales", "name": "bookings", "definition": "Value of signed contracts"},
    {"context": "finance", "name": "recognized_revenue", "definition": "Per ASC 606"}
  ],
  "synonyms": ["income", "sales"],
  "owner": "finance_operations"
}', '{"domain": "finance", "certification_tier": 2}'),

('ar_g_002', 'glossary_term', '{
  "canonical_name": "APAC",
  "display_name": "Asia-Pacific",
  "definition": "Asia-Pacific region for finance reporting",
  "variations": [
    {"context": "finance", "countries": ["JP", "KR", "SG", "HK", "TW", "AU", "NZ", "IN", "CN"]},
    {"context": "sales", "countries": ["JP", "KR", "SG", "HK", "TW", "IN", "CN"]}
  ],
  "synonyms": ["Asia-Pacific", "APAC region"],
  "owner": "finance_operations"
}', '{"domain": "reference"}'),

('ar_g_003', 'glossary_term', '{
  "canonical_name": "net_revenue",
  "display_name": "Net Revenue",
  "definition": "Recognized revenue per ASC 606 minus refunds",
  "synonyms": ["revenue net", "net sales"],
  "owner": "finance_operations"
}', '{"domain": "finance", "certification_tier": 1}'),

('ar_tk_001', 'tribal_knowledge', '{
  "type": "known_issue",
  "scope": {"tables": ["finance.fact_revenue_daily"], "dimensions": {"region": "APAC", "fiscal_period": "2019-Q4"}},
  "description": "Q4 2019 APAC data is incomplete",
  "reason": "Oracle to Snowflake migration caused data loss",
  "impact": "Revenue underreported by approximately 15%",
  "workaround": "Use Q4 2018 growth-adjusted estimate for trend analysis",
  "discovered_by": "maria.chen@company.com",
  "verified": true
}', '{"severity": "high", "active": true}'),

('ar_dc_001', 'data_contract', '{
  "name": "fact_revenue_daily",
  "owner": {"team": "finance_data_engineering", "contact": "fin-data@company.com"},
  "source": {"platform": "postgres", "schema": "finance", "table": "fact_revenue_daily"},
  "sla": {"freshness_hours": 6, "availability_pct": 99.5},
  "quality_rules": [
    {"rule": "transaction_id is unique", "severity": "critical"},
    {"rule": "amount >= 0", "severity": "warning"}
  ]
}', '{"last_validated": "2025-01-15"}'),

('ar_vr_001', 'validation_rule', '{
  "id": "revenue_non_negative",
  "description": "Revenue amount must be non-negative",
  "expression": "amount >= 0",
  "severity": "critical",
  "scope": ["net_revenue", "gross_revenue"]
}', '{"domain": "finance"}'),

('ar_cal_001', 'calendar_config', '{
  "calendar_type": "fiscal",
  "fiscal_year_start_month": 4,
  "quarters": {"Q1": [4,5,6], "Q2": [7,8,9], "Q3": [10,11,12], "Q4": [1,2,3]},
  "description": "April fiscal year; Q3 = Oct-Dec"
}', '{"domain": "reference"}'),

('ar_m_001', 'metric', '{
  "id": "net_revenue",
  "name": "Net Revenue",
  "semantic_layer_ref": "cube.finance.Revenue.netRevenue",
  "definition": "Recognized revenue per ASC 606 minus refunds",
  "dimensions": ["region", "fiscalPeriod", "transactionDate"],
  "owner": "finance_operations"
}', '{"domain": "finance", "certification_tier": 1}')
ON CONFLICT (id) DO UPDATE SET content = EXCLUDED.content, metadata = EXCLUDED.metadata, updated_at = NOW();
