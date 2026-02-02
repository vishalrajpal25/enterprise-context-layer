// Cube schema - Revenue cube against synthetic DW (fact_revenue_daily, dim_region)
cube('Revenue', {
  sql: `SELECT f.*, r.region_name FROM fact_revenue_daily f JOIN dim_region r ON f.region_code = r.region_code WHERE f.type = 'recognized'`,

  measures: {
    netRevenue: {
      sql: 'amount',
      type: 'sum',
      meta: {
        certification_tier: 1,
        definition: 'Recognized revenue per ASC 606 minus refunds',
      },
    },
    count: {
      type: 'count',
    },
  },

  dimensions: {
    region: {
      sql: 'region_code',
      type: 'string',
      meta: {
        variations: {
          finance: ['JP', 'KR', 'SG', 'HK', 'TW', 'AU', 'NZ', 'IN', 'CN'],
          sales: ['JP', 'KR', 'SG', 'HK', 'TW', 'IN', 'CN'],
        },
      },
    },
    fiscalPeriod: {
      sql: 'fiscal_period',
      type: 'string',
    },
    transactionDate: {
      sql: 'transaction_date',
      type: 'time',
    },
  },
});
