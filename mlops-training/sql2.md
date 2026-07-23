For your **Customer Churn Prediction** project, here are more in-depth SQL examples that resemble real interview and production scenarios.

---

### 1. Top 10 Customers by Total Purchase

```sql
SELECT
    c.customer_id,
    c.first_name,
    SUM(o.total_amount) AS total_spent
FROM customers c
JOIN orders o
ON c.customer_id = o.customer_id
GROUP BY c.customer_id,c.first_name
ORDER BY total_spent DESC
LIMIT 10;
```

---

### 2. Number of Orders per Customer

```sql
SELECT
    c.customer_id,
    c.first_name,
    COUNT(o.order_id) AS total_orders
FROM customers c
LEFT JOIN orders o
ON c.customer_id=o.customer_id
GROUP BY c.customer_id,c.first_name
ORDER BY total_orders DESC;
```

---

### 3. Customers Who Never Ordered

```sql
SELECT
    c.customer_id,
    c.first_name
FROM customers c
LEFT JOIN orders o
ON c.customer_id=o.customer_id
WHERE o.order_id IS NULL;
```

---

### 4. Highest Selling Product

```sql
SELECT
    p.product_name,
    COUNT(*) AS sold_count
FROM products p
JOIN orders o
ON p.product_id=o.product_id
GROUP BY p.product_name
ORDER BY sold_count DESC
LIMIT 1;
```

---

### 5. Revenue by Product

```sql
SELECT
    p.product_name,
    SUM(o.total_amount) AS revenue
FROM products p
JOIN orders o
ON p.product_id=o.product_id
GROUP BY p.product_name
ORDER BY revenue DESC;
```

---

### 6. Average Order Value

```sql
SELECT
AVG(total_amount) AS average_order
FROM orders;
```

---

### 7. Customers Spending More Than ₹50,000

```sql
SELECT
c.customer_id,
c.first_name,
SUM(o.total_amount) AS total_amount
FROM customers c
JOIN orders o
ON c.customer_id=o.customer_id
GROUP BY c.customer_id,c.first_name
HAVING SUM(o.total_amount)>50000;
```

---

### 8. State-wise Customer Count

```sql
SELECT
state,
COUNT(*) AS total_customers
FROM customers
GROUP BY state
ORDER BY total_customers DESC;
```

---

### 9. Monthly Sales

```sql
SELECT
DATE_TRUNC('month',order_date) AS month,
SUM(total_amount) AS sales
FROM orders
GROUP BY month
ORDER BY month;
```

---

### 10. Top 5 Cities by Revenue

```sql
SELECT
c.city,
SUM(o.total_amount) AS revenue
FROM customers c
JOIN orders o
ON c.customer_id=o.customer_id
GROUP BY c.city
ORDER BY revenue DESC
LIMIT 5;
```

---

### 11. Churn Customers

```sql
SELECT
c.customer_id,
c.first_name,
p.churn_probability
FROM customers c
JOIN predictions p
ON c.customer_id=p.customer_id
WHERE p.prediction='CHURN';
```

---

### 12. High Risk Customers

```sql
SELECT
customer_id,
prediction,
churn_probability
FROM predictions
WHERE churn_probability>80
ORDER BY churn_probability DESC;
```

---

### 13. Category-wise Sales

```sql
SELECT
p.category,
SUM(o.total_amount) AS revenue
FROM products p
JOIN orders o
ON p.product_id=o.product_id
GROUP BY p.category
ORDER BY revenue DESC;
```

---

### 14. Products Never Sold

```sql
SELECT
p.product_name
FROM products p
LEFT JOIN orders o
ON p.product_id=o.product_id
WHERE o.order_id IS NULL;
```

---

### 15. Customers with More Than 5 Orders

```sql
SELECT
c.customer_id,
c.first_name,
COUNT(*) AS total_orders
FROM customers c
JOIN orders o
ON c.customer_id=o.customer_id
GROUP BY c.customer_id,c.first_name
HAVING COUNT(*)>5;
```

---

### 16. Second Highest Product Price

```sql
SELECT DISTINCT price
FROM products
ORDER BY price DESC
OFFSET 1
LIMIT 1;
```

---

### 17. Top 3 Expensive Products

```sql
SELECT
product_name,
price
FROM products
ORDER BY price DESC
LIMIT 3;
```

---

### 18. Revenue by Payment Status

```sql
SELECT
payment_status,
SUM(total_amount) AS revenue
FROM orders
GROUP BY payment_status;
```

---

### 19. Customer Age Statistics

```sql
SELECT
MIN(age) AS minimum_age,
MAX(age) AS maximum_age,
AVG(age) AS average_age
FROM customers;
```

---

### 20. Customers Registered in Last 30 Days

```sql
SELECT *
FROM customers
WHERE signup_date>=CURRENT_DATE-30;
```

---

### 21. Top 10 Customers with Highest Churn Probability

```sql
SELECT
c.first_name,
p.churn_probability
FROM customers c
JOIN predictions p
ON c.customer_id=p.customer_id
ORDER BY p.churn_probability DESC
LIMIT 10;
```

---

### 22. Ranking Customers by Revenue (Window Function)

```sql
SELECT
c.customer_id,
c.first_name,
SUM(o.total_amount) AS revenue,
RANK() OVER(ORDER BY SUM(o.total_amount) DESC) AS customer_rank
FROM customers c
JOIN orders o
ON c.customer_id=o.customer_id
GROUP BY c.customer_id,c.first_name;
```

---

### 23. Running Total of Sales

```sql
SELECT
order_date,
total_amount,
SUM(total_amount)
OVER(ORDER BY order_date) AS running_total
FROM orders;
```

---

### 24. Find Duplicate Email Addresses

```sql
SELECT
email,
COUNT(*)
FROM customers
GROUP BY email
HAVING COUNT(*)>1;
```

---

### 25. Top Product in Each Category (Window Function)

```sql
SELECT *
FROM (
    SELECT
        category,
        product_name,
        price,
        ROW_NUMBER() OVER(
            PARTITION BY category
            ORDER BY price DESC
        ) AS rn
    FROM products
) t
WHERE rn = 1;
```

These examples introduce concepts like aggregation, joins, subqueries, window functions, ranking, and analytics. They are excellent practice for SQL interviews and form the basis for feature engineering and reporting in an MLOps customer churn prediction project.
