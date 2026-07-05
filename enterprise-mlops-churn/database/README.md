# Module 3-A: SQL Data Source (PostgreSQL / Amazon RDS)

Extends Module 3 (Data Engineering & Feature Engineering) to cover the
**"SQL Data Sources"** topic using a real PostgreSQL database instead of
a flat CSV — either a local Postgres instance for practice, or Amazon
RDS for PostgreSQL for the enterprise-realistic version.

---

## What this lab builds

```
generate_seed_data.py  →  seed_customers.csv  (1,000 Indian-name customer records)
                                  ↓
                          load_data.py
                                  ↓
                  PostgreSQL: ml_ops_db → churn.customers table
                                  ↓
        (Module 3 pipeline can later SELECT * FROM churn.customers
         instead of reading data/raw/customer_churn.csv directly)
```

---

## ⚠️ A note on the endpoint format you gave

You wrote:
```
mydbinstance.c7tj4example.us-east-1.rds.amazonaws.com:3306
```
That's the correct **shape** of an RDS endpoint, but `:3306` is the
**MySQL/Aurora-MySQL** default port. For an RDS instance provisioned
with the **PostgreSQL** engine (which is what you asked for), the
default port is **`5432`**. This module's scripts and `.env.example`
use `5432`. If your actual RDS instance really is MySQL, say so and
I'll give you a MySQL-flavored version of this module instead — the
schema and Python logic barely change.

---

## Step 1 — Create the database, role, and schema

Run as the RDS **master user** (or local `postgres` superuser):

```bash
psql -h <endpoint> -p 5432 -U <master_user> -d postgres -f schema.sql
```

`schema.sql` creates:
- Database `ml_ops_db`
- Least-privilege role `ml_user` (application code never uses the master user)
- Schema `churn` owned by `ml_user`
- Table `churn.customers` matching the ML pipeline's feature set, plus Indian-context columns (`city`, `state`, INR pricing)

### About the password

`schema.sql` ships with a placeholder strong password:
```
ChurnDB_2026_!Xk7pQ9vR
```
This is a **suggested example only** — 22 characters, upper/lower/digits/symbols, no dictionary words. Treat it the way you'd treat any credential in a course repo: **rotate it before using a real database**, and never commit the real value to Git. Generate your own with:

```bash
python3 -c "import secrets, string; a=string.ascii_letters+string.digits+'!@#%^&*'; print(''.join(secrets.choice(a) for _ in range(24)))"
# or
openssl rand -base64 24
```

Then either edit `schema.sql` before running it, or run `ALTER ROLE ml_user WITH PASSWORD '<new-password>';` afterward.

---

## Step 2 — Configure credentials

```bash
cp .env.example .env
# edit .env with your real DB_HOST / DB_PASSWORD
export $(grep -v '^#' .env | xargs)
```

For a **local** Postgres instance instead of RDS, set `DB_HOST=127.0.0.1` and `DB_SSLMODE=prefer`. For **RDS**, keep `DB_SSLMODE=require`.

---

## Step 3 — Install dependencies

```bash
pip install -r requirements-db.txt
```

---

## Step 4 — Generate 1,000 Indian-name customer records

```bash
python generate_seed_data.py --count 1000 --out seed_customers.csv
```

Uses `Faker("en_IN")` for realistic Indian names, paired with 12 Indian states/cities and INR-scaled pricing (₹299–₹2,999/month). Churn likelihood follows the same logic as the core project's dataset (month-to-month + fiber + low tenure + high charges → higher churn), so the data is statistically consistent with `data/raw/customer_churn.csv`.

---

## Step 5 — Load into PostgreSQL

```bash
python load_data.py --csv seed_customers.csv
```

Expected output:
```
Inserted (or skipped existing) 1000 rows into churn.customers
Total rows in table: 1000
Churn breakdown: [('No', 391), ('Yes', 609)]
```

The load is idempotent — re-running it won't duplicate rows (`ON CONFLICT (customer_id) DO NOTHING`).

---

## Step 6 — Verify

```bash
psql -h <endpoint> -p 5432 -U ml_user -d ml_ops_db
```
```sql
SELECT count(*) FROM churn.customers;
SELECT churn, count(*) FROM churn.customers GROUP BY churn;
SELECT state, count(*) FROM churn.customers GROUP BY state ORDER BY 2 DESC;
```

---

## Connecting this back to the core ML pipeline

`src/data_ingestion.py` currently reads from a CSV path in `config/config.yaml`. To source from this database instead, swap `load_raw_data()` for a query like:

```python
import pandas as pd
import psycopg2

def load_raw_data_from_db():
    conn = psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME,
        user=DB_USER, password=DB_PASSWORD, sslmode=DB_SSLMODE,
    )
    return pd.read_sql("SELECT * FROM churn.customers;", conn)
```

This is the natural bridge from Module 3-A into Module 5 (DVC) and Module 13 (AWS/SageMaker) — the database becomes the system of record, and DVC/S3 versions *exports* of it rather than the raw CSV.

---

## Files in this module

| File | Purpose |
|---|---|
| `schema.sql` | Database, role, schema, and table DDL |
| `generate_seed_data.py` | Generates 1,000 Indian-name synthetic customer records |
| `load_data.py` | Loads the CSV into PostgreSQL via `psycopg2` |
| `requirements-db.txt` | `psycopg2-binary`, `faker`, `python-dotenv` |
| `.env.example` | Credential template — copy to `.env`, never commit the real file |
