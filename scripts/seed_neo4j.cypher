// Knowledge Graph seed - entities, metrics, glossary terms, lineage stubs
// Run via neo4j shell or Browser

// Clear existing (optional - remove in prod)
MATCH (n) DETACH DELETE n;

// Ontology: Region and Entity
CREATE (r:Entity {id: 'region', name: 'Region', domain: 'reference'});
CREATE (c:Entity {id: 'customer', name: 'Customer', domain: 'sales'});

// Region APAC
CREATE (apac:Region {id: 'region_apac', code: 'APAC', name: 'Asia-Pacific'});
CREATE (apac)-[:HAS_VARIATION {context: 'finance'}]->(v1:Variation {countries: ['JP', 'KR', 'SG', 'HK', 'TW', 'AU', 'NZ', 'IN', 'CN']});
CREATE (apac)-[:HAS_VARIATION {context: 'sales'}]->(v2:Variation {countries: ['JP', 'KR', 'SG', 'HK', 'TW', 'IN', 'CN']});

// Glossary term: revenue
CREATE (g:GlossaryTerm {id: 'revenue', asset_registry_id: 'ar_g_001', name: 'revenue'});

// Metrics
CREATE (m1:Metric {id: 'net_revenue', name: 'Net Revenue', semantic_layer_ref: 'cube.finance.Revenue.netRevenue', asset_registry_id: 'ar_m_001', certification_tier: 1});
CREATE (m1)-[:DEFINED_BY]->(g);

CREATE (m2:Metric {id: 'budget_net_revenue', name: 'Budget Net Revenue', semantic_layer_ref: 'cube.planning.Budget.netRevenueBudget', certification_tier: 2});
CREATE (m2)-[:FOR_METRIC]->(m1);

// Dimension: region
CREATE (d:Dimension {id: 'region', name: 'region'});
CREATE (m1)-[:USES_DIMENSION]->(d);
CREATE (d)-[:MAPS_TO]->(r);

// Tribal knowledge
CREATE (tk:TribalKnowledge {id: 'tk_001', asset_registry_id: 'ar_tk_001', scope_regions: ['APAC'], scope_periods: ['2019-Q4']});
CREATE (m1)-[:HAS_KNOWN_ISSUE]->(tk);

// Lineage stub: metric -> column
CREATE (col:Column {id: 'analytics.finance.fact_revenue_daily.amount'});
CREATE (m1)-[:COMPUTED_FROM]->(col);
CREATE (src:Column {id: 'raw.erp.gl.amount'});
CREATE (col)-[:TRANSFORMS_FROM]->(src);
