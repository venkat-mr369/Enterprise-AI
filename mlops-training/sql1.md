Using the **customers**, **products**, **orders**, and **predictions** tables, here are practical SQL examples.

### SELECT

```sql
SELECT * FROM customers;
```

```sql
SELECT first_name, email
FROM customers;
```

---

### WHERE

```sql
SELECT *
FROM customers
WHERE city = 'City1';
```

```sql
SELECT *
FROM products
WHERE price > 1000;
```

---

### ORDER BY

```sql
SELECT *
FROM products
ORDER BY price DESC;
```

```sql
SELECT *
FROM customers
ORDER BY signup_date ASC;
```

---

### GROUP BY

```sql
SELECT city,
COUNT(*) AS total_customers
FROM customers
GROUP BY city;
```

```sql
SELECT payment_status,
COUNT(*) AS total_orders
FROM orders
GROUP BY payment_status;
```

---

### HAVING

Show only cities having more than 50 customers.

```sql
SELECT city,
COUNT(*) AS total_customers
FROM customers
GROUP BY city
HAVING COUNT(*) > 50;
```

Show payment status having more than 100 orders.

```sql
SELECT payment_status,
COUNT(*)
FROM orders
GROUP BY payment_status
HAVING COUNT(*) > 100;
```

---

### LIMIT

```sql
SELECT *
FROM customers
LIMIT 10;
```

Top 5 expensive products.

```sql
SELECT *
FROM products
ORDER BY price DESC
LIMIT 5;
```

---

### DISTINCT

```sql
SELECT DISTINCT city
FROM customers;
```

```sql
SELECT DISTINCT category
FROM products;
```

---

### INNER JOIN

```sql
SELECT
o.order_id,
c.first_name,
p.product_name,
o.total_amount
FROM orders o
JOIN customers c
ON o.customer_id = c.customer_id
JOIN products p
ON o.product_id = p.product_id;
```

---

### LEFT JOIN

Show all customers even if they have no orders.

```sql
SELECT
c.customer_id,
c.first_name,
o.order_id
FROM customers c
LEFT JOIN orders o
ON c.customer_id = o.customer_id;
```

---

### RIGHT JOIN

```sql
SELECT
c.first_name,
o.order_id
FROM customers c
RIGHT JOIN orders o
ON c.customer_id = o.customer_id;
```

---

### FULL OUTER JOIN

```sql
SELECT
c.first_name,
o.order_id
FROM customers c
FULL OUTER JOIN orders o
ON c.customer_id = o.customer_id;
```

---

### UNION

```sql
SELECT city
FROM customers

UNION

SELECT category
FROM products;
```

---

### UNION ALL

```sql
SELECT city
FROM customers

UNION ALL

SELECT category
FROM products;
```

---

### Aggregate Functions

#### COUNT

```sql
SELECT COUNT(*)
FROM customers;
```

#### SUM

```sql
SELECT SUM(total_amount)
FROM orders;
```

#### AVG

```sql
SELECT AVG(price)
FROM products;
```

#### MAX

```sql
SELECT MAX(price)
FROM products;
```

#### MIN

```sql
SELECT MIN(price)
FROM products;
```

---

### Multiple Conditions

```sql
SELECT *
FROM customers
WHERE city='City1'
AND status='ACTIVE';
```

---

### BETWEEN

```sql
SELECT *
FROM products
WHERE price BETWEEN 500 AND 2000;
```

---

### IN

```sql
SELECT *
FROM customers
WHERE city IN ('City1','City2','City3');
```

---

### LIKE

```sql
SELECT *
FROM customers
WHERE first_name LIKE 'Customer1%';
```

---

### IS NULL

```sql
SELECT *
FROM predictions
WHERE prediction IS NULL;
```

---

### Alias

```sql
SELECT
customer_id AS ID,
first_name AS CustomerName
FROM customers;
```

These examples cover the core SQL concepts typically taught in beginner-to-intermediate database courses and are directly applicable to your customer prediction project.
