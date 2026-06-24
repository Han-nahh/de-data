-- Stage and normalize acquired PostgreSQL source rows.

DROP TABLE IF EXISTS stg_acquired_cleaned;

CREATE TABLE stg_acquired_cleaned AS
SELECT 
    'acquired' AS source_system,
    p.id AS source_transaction_id,
    'acquired:' || p.id AS warehouse_transaction_id,
    CASE 
        WHEN p.sale_date LIKE '%/%' THEN 
            SUBSTR(p.sale_date, 7, 4) || '-' || SUBSTR(p.sale_date, 4, 2) || '-' || SUBSTR(p.sale_date, 1, 2) || ' ' || SUBSTR(p.sale_date, 12, 8)
        ELSE p.sale_date
    END AS checkout_timestamp,
    CAST(p.customer_id AS TEXT) AS customer_id,
    '' AS customer_country,
    REPLACE(REPLACE(p.product_sku, 'PROD-', ''), 'SKU-', '') AS sku,
    ROUND(CAST(p.total_price AS REAL) * CAST(er.rate_to_usd AS REAL), 2) AS gross_amount_usd,
    0.00 AS tax_amount_usd,
    'false' AS is_refunded
FROM stg_postgres_sales p
LEFT JOIN stg_exchange_rates er ON p.currency = er.currency
WHERE p.id IS NOT NULL 
  AND er.rate_to_usd IS NOT NULL
  AND p.id NOT IN (SELECT id FROM stg_postgres_sales WHERE id IS NOT NULL GROUP BY id HAVING COUNT(*) > 1 AND rowid > (SELECT MIN(rowid) FROM stg_postgres_sales ps WHERE ps.id = stg_postgres_sales.id));

DROP TABLE IF EXISTS acquired_rejects;
CREATE TABLE acquired_rejects AS
SELECT 
    'acquired' AS source_system,
    p.id AS source_transaction_id,
    'unknown_currency' AS reject_reason
FROM stg_postgres_sales p
LEFT JOIN stg_exchange_rates er ON p.currency = er.currency
WHERE p.id IS NOT NULL AND er.rate_to_usd IS NULL
UNION ALL
SELECT 
    'acquired' AS source_system,
    p.id AS source_transaction_id,
    'duplicate_source_transaction' AS reject_reason
FROM stg_postgres_sales p
WHERE p.id IS NOT NULL 
  AND p.rowid > (SELECT MIN(ps.rowid) FROM stg_postgres_sales ps WHERE ps.id = p.id);