For a customer churn prediction project, these four tables are a good foundation:

* `customers`
* `products`
* `orders`
* `predictions`

Instead of writing 1,000 individual `INSERT` statements, PostgreSQL can generate realistic demo data using `generate_series()`. This is much faster and is commonly used for training and testing.

### Create Customers

```sql
CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100) UNIQUE,
    gender VARCHAR(10),
    age INT,
    city VARCHAR(50),
    state VARCHAR(50),
    signup_date DATE,
    status VARCHAR(20)
);
```

### Insert 1,000 Customers

```sql
INSERT INTO customers
(first_name,last_name,email,gender,age,city,state,signup_date,status)
SELECT
'Customer'||g,
'Last'||g,
'customer'||g||'@gmail.com',
CASE WHEN g%2=0 THEN 'Male' ELSE 'Female' END,
18+(random()*42)::INT,
'City'||((g%20)+1),
'State'||((g%10)+1),
CURRENT_DATE-(random()*1000)::INT,
CASE WHEN random()>0.2 THEN 'ACTIVE' ELSE 'INACTIVE' END
FROM generate_series(1,1000) g;
```

---

### Create Products

```sql
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50),
    price NUMERIC(10,2),
    stock_quantity INT
);
```

### Insert 1,000 Products

```sql
INSERT INTO products
(product_name,category,price,stock_quantity)
SELECT
'Product'||g,
'Category'||((g%10)+1),
ROUND((50+random()*5000)::numeric,2),
(random()*500)::INT
FROM generate_series(1,1000) g;
```

---

### Create Orders

```sql
CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id),
    product_id INT REFERENCES products(product_id),
    quantity INT,
    total_amount NUMERIC(10,2),
    order_date TIMESTAMP,
    payment_status VARCHAR(20)
);
```

### Insert 1,000 Orders

```sql
INSERT INTO orders
(customer_id,product_id,quantity,total_amount,order_date,payment_status)
SELECT
(random()*999+1)::INT,
(random()*999+1)::INT,
(random()*5+1)::INT,
ROUND((100+random()*10000)::numeric,2),
NOW()-(random()*365||' days')::INTERVAL,
CASE
    WHEN random()>0.1 THEN 'PAID'
    ELSE 'PENDING'
END
FROM generate_series(1,1000);
```

---

### Create Predictions

```sql
CREATE TABLE predictions (
    prediction_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id),
    churn_probability NUMERIC(5,2),
    prediction VARCHAR(20),
    model_version VARCHAR(20),
    prediction_time TIMESTAMP
);
```

### Insert 1,000 Predictions

```sql
INSERT INTO predictions
(customer_id,churn_probability,prediction,model_version,prediction_time)
SELECT
g,
ROUND((random()*100)::numeric,2),
CASE
    WHEN random()>0.7 THEN 'CHURN'
    ELSE 'NO_CHURN'
END,
'v1.0',
NOW()-(random()*30||' days')::INTERVAL
FROM generate_series(1,1000) g;
```

After running these scripts, you'll have:

| Table       | Records |
| ----------- | ------- |
| customers   | 1,000   |
| products    | 1,000   |
| orders      | 1,000   |
| predictions | 1,000   |

For an enterprise MLOps course, I recommend expanding this to **10–12 related tables** (customers, addresses, products, categories, orders, order_items, payments, customer_activity, support_tickets, predictions, model_registry, and prediction_logs). This provides a much more realistic dataset for SQL, ML feature engineering, FastAPI, PostgreSQL, and MLOps labs.
