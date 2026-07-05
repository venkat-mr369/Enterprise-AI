-- =====================================================================
-- Module 3-A: PostgreSQL Data Source for Enterprise MLOps
-- =====================================================================
-- Target: Amazon RDS for PostgreSQL
--   Example endpoint format:
--   mydbinstance.c7tj4example.us-east-1.rds.amazonaws.com:5432
--
-- NOTE ON PORTS: PostgreSQL's default port is 5432, not 3306.
-- Port 3306 is the MySQL/Aurora-MySQL default. If your RDS instance
-- was provisioned as a MySQL/MariaDB engine, use the mysql client and
-- Module 3-B (MySQL) scripts instead. This module assumes a PostgreSQL
-- engine instance, listening on 5432.
--
-- Run this file as a superuser (e.g. the RDS master user) BEFORE
-- running generate_seed_data.py / load_data.py.
-- =====================================================================

-- 1. Create the application database
--    (Postgres identifiers with hyphens must be double-quoted every time
--     they're referenced, which is error-prone in scripts/ORMs. We use
--     the underscore form "ml_ops_db" as the real object name and note
--     the hyphenated form your team may refer to it by informally.)
CREATE DATABASE ml_ops_db;

-- Connect to it before continuing:
--   psql -h <endpoint> -p 5432 -U <master_user> -d ml_ops_db

-- 2. Create a dedicated least-privilege application role
--    Do not use the RDS master user in application code.
CREATE ROLE ml_user WITH LOGIN PASSWORD 'ChurnDB_2026_!Xk7pQ9vR';
ALTER ROLE ml_user SET statement_timeout = '30s';

-- 3. Grant only what the app/pipeline needs on this database
GRANT CONNECT ON DATABASE ml_ops_db TO ml_user;

\c ml_ops_db

CREATE SCHEMA IF NOT EXISTS churn AUTHORIZATION ml_user;
GRANT USAGE, CREATE ON SCHEMA churn TO ml_user;

-- 4. Core customer table — mirrors the feature set used by
--    src/data_ingestion.py / src/preprocessing.py in the ML pipeline,
--    with an Indian-market customer roster for this course.
CREATE TABLE IF NOT EXISTS churn.customers (
    customer_id         VARCHAR(20)   PRIMARY KEY,
    full_name            VARCHAR(120)  NOT NULL,
    gender               VARCHAR(10)   NOT NULL CHECK (gender IN ('Male', 'Female')),
    senior_citizen       SMALLINT      NOT NULL CHECK (senior_citizen IN (0, 1)),
    partner              VARCHAR(3)    NOT NULL CHECK (partner IN ('Yes', 'No')),
    dependents           VARCHAR(3)    NOT NULL CHECK (dependents IN ('Yes', 'No')),
    city                 VARCHAR(60)   NOT NULL,
    state                VARCHAR(60)   NOT NULL,
    tenure_months        INTEGER       NOT NULL CHECK (tenure_months >= 0),
    internet_service     VARCHAR(20)   NOT NULL CHECK (internet_service IN ('DSL', 'Fiber optic', 'No')),
    contract             VARCHAR(20)   NOT NULL CHECK (contract IN ('Month-to-month', 'One year', 'Two year')),
    paperless_billing    VARCHAR(3)    NOT NULL CHECK (paperless_billing IN ('Yes', 'No')),
    payment_method       VARCHAR(30)   NOT NULL,
    monthly_charges_inr  NUMERIC(10,2) NOT NULL CHECK (monthly_charges_inr >= 0),
    total_charges_inr    NUMERIC(12,2) NOT NULL CHECK (total_charges_inr >= 0),
    churn                VARCHAR(3)    NOT NULL CHECK (churn IN ('Yes', 'No')),
    created_at           TIMESTAMPTZ   NOT NULL DEFAULT now()
);

-- Helpful indexes for the query patterns Module 3/4 labs will use
CREATE INDEX IF NOT EXISTS idx_customers_churn    ON churn.customers (churn);
CREATE INDEX IF NOT EXISTS idx_customers_contract ON churn.customers (contract);
CREATE INDEX IF NOT EXISTS idx_customers_state    ON churn.customers (state);

-- 5. Hand ownership + future-table defaults to ml_user so the loader
--    script (running as ml_user) can INSERT without extra grants
ALTER TABLE churn.customers OWNER TO ml_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA churn GRANT ALL ON TABLES TO ml_user;

-- =====================================================================
-- Verification queries (run after load_data.py populates ~1000 rows)
-- =====================================================================
-- SELECT count(*) FROM churn.customers;
-- SELECT churn, count(*) FROM churn.customers GROUP BY churn;
-- SELECT state, count(*) FROM churn.customers GROUP BY state ORDER BY 2 DESC;
