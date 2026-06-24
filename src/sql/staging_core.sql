-- Stage and normalize core SQL Server source rows.

DROP TABLE IF EXISTS stg_core_cleaned;

CREATE TABLE stg_core_cleaned AS
SELECT 
    'core' AS source_system,
    s.tx_id AS source_transaction_id,
    'core:' || s.tx_id AS warehouse_transaction_id,
    s.checkout_timestamp AS checkout_timestamp,
    CAST(json_extract(s.customer_blob, '$.id') AS TEXT) AS customer_id,
    CAST(json_extract(s.customer_blob, '$.country') AS TEXT) AS customer_country,
    REPLACE(REPLACE(s.sku_code, 'PROD-', ''), 'SKU-', '') AS sku,
    CAST(s.gross_amt_usd AS REAL) AS gross_amount_usd,
    CAST(s.tax_amt AS REAL) AS tax_amount_usd,
    CASE WHEN CAST(s.is_refunded AS INTEGER) = 1 THEN 'true' ELSE 'false' END AS is_refunded
FROM stg_sqlserver_sales s
WHERE s.tx_id IS NOT NULL 
  AND json_valid(s.customer_blob) = 1
  AND s.sku_code IS NOT NULL 
  AND s.sku_code != '';

DROP TABLE IF EXISTS core_rejects;
CREATE TABLE core_rejects AS
SELECT 
    'core' AS source_system,
    tx_id AS source_transaction_id,
    CASE 
        WHEN tx_id IS NULL THEN 'missing_transaction_id'
        WHEN json_valid(customer_blob) = 0 THEN 'invalid_customer_blob'
        WHEN sku_code IS NULL OR sku_code = '' THEN 'missing_sku'
        ELSE 'invalid_data'
    END AS reject_reason
FROM stg_sqlserver_sales
WHERE tx_id IS NULL 
   OR json_valid(customer_blob) = 0 
   OR sku_code IS NULL 
   OR sku_code = '';