"""
load_data.py
------------
Loads seed_customers.csv into PostgreSQL (churn.customers table) on
either a local instance or an Amazon RDS for PostgreSQL endpoint.

Reads connection details from environment variables so credentials
never get hardcoded or committed to Git. Copy .env.example to .env
and fill in real values, or export the variables directly.

Usage:
    python generate_seed_data.py --count 1000 --out seed_customers.csv
    python load_data.py --csv seed_customers.csv
"""

import argparse
import csv
import os
import sys

import psycopg2
from psycopg2.extras import execute_values


def get_connection():
    host = os.environ.get("DB_HOST", "localhost")
    port = os.environ.get("DB_PORT", "5432")
    dbname = os.environ.get("DB_NAME", "ml_ops_db")
    user = os.environ.get("DB_USER", "ml_user")
    password = os.environ.get("DB_PASSWORD")

    if not password:
        sys.exit(
            "DB_PASSWORD is not set. Copy database/.env.example to .env, "
            "fill in a real password, then `export $(cat .env | xargs)` "
            "or use python-dotenv before running this script."
        )

    return psycopg2.connect(
        host=host, port=port, dbname=dbname, user=user, password=password,
        sslmode=os.environ.get("DB_SSLMODE", "prefer"),  # RDS: set to 'require'
    )


INSERT_SQL = """
INSERT INTO churn.customers (
    customer_id, full_name, gender, senior_citizen, partner, dependents,
    city, state, tenure_months, internet_service, contract,
    paperless_billing, payment_method, monthly_charges_inr,
    total_charges_inr, churn
) VALUES %s
ON CONFLICT (customer_id) DO NOTHING;
"""


def load_csv(path: str, conn) -> int:
    with open(path, "r") as f:
        reader = csv.DictReader(f)
        rows = [
            (
                r["customer_id"], r["full_name"], r["gender"],
                int(r["senior_citizen"]), r["partner"], r["dependents"],
                r["city"], r["state"], int(r["tenure_months"]),
                r["internet_service"], r["contract"], r["paperless_billing"],
                r["payment_method"], float(r["monthly_charges_inr"]),
                float(r["total_charges_inr"]), r["churn"],
            )
            for r in reader
        ]

    with conn.cursor() as cur:
        execute_values(cur, INSERT_SQL, rows, page_size=200)
    conn.commit()
    return len(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", type=str, default="seed_customers.csv")
    args = parser.parse_args()

    conn = get_connection()
    try:
        inserted = load_csv(args.csv, conn)
        print(f"Inserted (or skipped existing) {inserted} rows into churn.customers")

        with conn.cursor() as cur:
            cur.execute("SELECT count(*) FROM churn.customers;")
            total = cur.fetchone()[0]
            cur.execute("SELECT churn, count(*) FROM churn.customers GROUP BY churn;")
            breakdown = cur.fetchall()

        print(f"Total rows in table: {total}")
        print(f"Churn breakdown: {breakdown}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
