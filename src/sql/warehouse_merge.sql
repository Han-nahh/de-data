-- Merge staged rows into final Snowflake fact and reject tables.

CREATE TABLE IF NOT EXISTS sales_fact (
    source_system TEXT,
    source_transaction_id TEXT,
    warehouse_transaction_id TEXT PRIMARY KEY,
    checkout_timestamp TEXT,
    customer_id TEXT,
    customer_country TEXT,
    sku TEXT,
    gross_amount_usd REAL,
    tax_amount_usd REAL,
    is_refunded TEXT
);

CREATE TABLE IF NOT EXISTS rejects_fact (
    source_system TEXT,
    source_transaction_id TEXT,
    reject_reason TEXT,
    PRIMARY KEY (source_system, source_transaction_id, reject_reason)
);

DROP TABLE IF EXISTS unified_staging;
CREATE TABLE unified_staging AS 
SELECT * FROM stg_core_cleaned
UNION ALL
SELECT * FROM stg_acquired_cleaned;

INSERT OR REPLACE INTO sales_fact 
SELECT * FROM unified_staging;

DROP TABLE IF EXISTS unified_rejects;
CREATE TABLE unified_rejects AS 
SELECT * FROM core_rejects
UNION ALL
SELECT * FROM acquired_rejects;

INSERT OR REPLACE INTO rejects_fact 
SELECT * FROM unified_rejects;