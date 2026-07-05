# Module 2 – Python Essentials for Enterprise MLOps

## Capstone Project

**Enterprise Customer Churn Prediction**

Business Problem

An e-commerce company wants to identify customers who are likely to stop purchasing products.

Our goal throughout this course is to build an end-to-end MLOps pipeline that predicts customer churn.

Dataset (sample columns)

| CustomerID | Age | Gender | City      | Orders | TotalSpend | LastPurchaseDays | CouponsUsed | AvgOrderValue | Returns | SupportTickets | Churn |
| ---------- | --- | ------ | --------- | ------ | ---------- | ---------------- | ----------- | ------------- | ------- | -------------- | ----- |
| 1001       | 28  | Male   | Hyderabad | 15     | 22000      | 15               | 4           | 1450          | 1       | 0              | 0     |
| 1002       | 42  | Female | Bangalore | 3      | 2800       | 120              | 0           | 900           | 3       | 5              | 1     |

Target Column

```
Churn

0 = Active Customer

1 = Churned Customer
```

---

# Learning Objectives

After completing this module students will be able to

* Write Python programs
* Read customer datasets
* Explore customer information
* Handle missing data
* Work with CSV files
* Use NumPy
* Use Pandas
* Visualize churn data
* Build reusable Python functions
* Prepare data for machine learning

---

# Why Python for MLOps?

Python is the most widely used programming language in Machine Learning and MLOps because it has a rich ecosystem of libraries, is easy to learn, and integrates well with cloud platforms, APIs, automation, and data engineering tools.

In our project, Python will be used for:

* Reading customer datasets
* Cleaning data
* Feature engineering
* Training ML models
* Building APIs
* Automating pipelines
* Monitoring models

---

# 1. Python Fundamentals

Python is an interpreted, high-level programming language.

Example:

```python
print("Welcome to Enterprise MLOps")
```

Output:

```
Welcome to Enterprise MLOps
```

### Our Project Example

```python
print("Customer Churn Prediction Project")
```

Output:

```
Customer Churn Prediction Project
```

---

# Comments in Python

Comments improve readability.

```python
# Load customer dataset

# Train model

# Deploy API
```

---

# Variables

Variables store information.

Example

```python
customer_name = "Ravi"
```

Project Example

```python
customer_id = 1001

total_spend = 24000

orders = 18

last_purchase_days = 22

churn = 0
```

Output

```
Customer ID :1001

Orders :18

Churn :0
```

---

# Variable Naming Rules

Good

```python
customer_name

total_spend

last_purchase_days
```

Bad

```python
1customer

total spend

class
```

---

# Data Types

Python supports multiple data types.

| Type  | Example     |
| ----- | ----------- |
| int   | 25          |
| float | 1999.50     |
| str   | "Hyderabad" |
| bool  | True        |
| list  | []          |
| dict  | {}          |

---

### Example

```python
customer_id = 1001

customer_name = "John"

avg_order = 899.55

active = True
```

Check type

```python
print(type(customer_name))
```

Output

```
<class 'str'>
```

---

# Operators

Arithmetic Operators

```python
orders = 20

returns = 2

net_orders = orders - returns

print(net_orders)
```

Output

```
18
```

Comparison Operators

```python
orders = 15

print(orders > 10)
```

Output

```
True
```

Logical Operators

```python
orders = 12

spend = 25000

print(orders > 10 and spend > 20000)
```

Output

```
True
```

---

# Conditional Statements

Suppose our business defines churn risk based on the last purchase date.

```python
last_purchase_days = 140

if last_purchase_days > 90:
    print("High Churn Risk")
else:
    print("Active Customer")
```

Output

```
High Churn Risk
```

---

### Multiple Conditions

```python
score = 82

if score >= 90:
    print("Gold Customer")

elif score >=70:
    print("Silver Customer")

else:
    print("Bronze Customer")
```

---

# Loops

Suppose we want to print all customer IDs.

```python
customers = [1001,1002,1003,1004]

for customer in customers:
    print(customer)
```

Output

```
1001

1002

1003

1004
```

---

### Loop Through Dataset

```python
orders = [15,8,20,4]

for order in orders:
    print(order)
```

---

# While Loop

```python
count = 1

while count<=5:
    print(count)
    count +=1
```

---

# Functions

Functions reduce code duplication.

Without Function

```python
print("Customer Churn Prediction")
print("Customer Churn Prediction")
print("Customer Churn Prediction")
```

With Function

```python
def welcome():

    print("Customer Churn Prediction")

welcome()
```

---

### Function with Parameters

```python
def customer_status(name,churn):

    if churn==1:
        print(name,"will churn")

    else:
        print(name,"active")

customer_status("John",1)
```

Output

```
John will churn
```

---

### Function Returning Values

```python
def average_order(total,orders):

    return total/orders

print(average_order(12000,12))
```

Output

```
1000
```

---

# Modules

Modules organize code into reusable files.

Suppose

```
utils.py
```

contains

```python
def greeting():

    print("Welcome")
```

Main Program

```python
import utils

utils.greeting()
```

---

# Lists

Lists store multiple values.

```python
cities=["Delhi","Hyderabad","Mumbai"]

print(cities)
```

Customer Example

```python
customers=[
1001,
1002,
1003,
1004
]
```

Access

```python
print(customers[2])
```

Output

```
1003
```

Append

```python
customers.append(1005)
```

---

# Dictionaries

Store data as key-value pairs.

```python
customer={
"ID":1001,
"City":"Hyderabad",
"Orders":15,
"Spend":25000
}
```

Access

```python
print(customer["Spend"])
```

Output

```
25000
```

---

# Exception Handling

Errors should be handled gracefully.

Without Exception

```python
average=100/0
```

Program crashes.

With Exception

```python
try:

    average=100/0

except ZeroDivisionError:

    print("Cannot divide by zero")
```

Project Example

```python
try:

    file=open("customer.csv")

except FileNotFoundError:

    print("Dataset not found")
```

---

# File Handling

Writing

```python
file=open("result.txt","w")

file.write("Customer Churn Model")

file.close()
```

Reading

```python
file=open("result.txt")

print(file.read())

file.close()
```

Using `with`

```python
with open("result.txt") as file:

    print(file.read())
```

---

# Virtual Environment

Why?

Every ML project should have isolated dependencies.

Create

```bash
python -m venv venv
```

Activate

Windows

```bash
venv\Scripts\activate
```

Linux/macOS

```bash
source venv/bin/activate
```

Verify

```bash
python --version
```

Deactivate

```bash
deactivate
```

---

# Pip

Install package

```bash
pip install pandas
```

Install multiple packages

```bash
pip install numpy matplotlib scikit-learn
```

Check

```bash
pip list
```

Freeze

```bash
pip freeze > requirements.txt
```

Install from file

```bash
pip install -r requirements.txt
```

---

# NumPy

NumPy provides efficient numerical computing using multidimensional arrays.

Create array

```python
import numpy as np

orders=np.array([15,10,12,18])
```

Average

```python
print(np.mean(orders))
```

Maximum

```python
print(np.max(orders))
```

Project Example

```python
spend=np.array([2500,3200,8900,12000])

print(np.mean(spend))
```

---

# Pandas

Pandas is the most important library for data manipulation in MLOps.

Import

```python
import pandas as pd
```

Read Dataset

```python
df=pd.read_csv("customers.csv")
```

View Data

```python
df.head()
```

Rows and Columns

```python
df.shape
```

Columns

```python
df.columns
```

Statistics

```python
df.describe()
```

Missing Values

```python
df.isnull().sum()
```

Filter Churned Customers

```python
df[df["Churn"]==1]
```

Average Spend

```python
df["TotalSpend"].mean()
```

Group by City

```python
df.groupby("City")["TotalSpend"].mean()
```

---

# Matplotlib

Visualizations help understand patterns before model training.

Import

```python
import matplotlib.pyplot as plt
```

Orders Distribution

```python
plt.hist(df["Orders"])
plt.title("Customer Orders")
plt.xlabel("Orders")
plt.ylabel("Customers")
plt.show()
```

Average Spend by City

```python
df.groupby("City")["TotalSpend"].mean().plot(kind="bar")

plt.show()
```

Scatter Plot

```python
plt.scatter(df["Orders"],df["TotalSpend"])

plt.xlabel("Orders")

plt.ylabel("Spend")
```

These charts help identify relationships between customer behavior and churn.

---

# Working with CSV Files

Read

```python
import pandas as pd

df = pd.read_csv("customers.csv")
```

Write

```python
df.to_csv("processed_customers.csv", index=False)
```

Select Columns

```python
df = df[["CustomerID","Orders","TotalSpend","Churn"]]
```

Save Processed Data

```python
df.to_csv("customer_clean.csv", index=False)
```

---

# Lab – Customer Dataset Exploration

## Objective

Perform initial exploration of the customer churn dataset and understand its quality before building ML models.

### Step 1: Load the Dataset

```python
import pandas as pd

df = pd.read_csv("customer_churn.csv")
```

### Step 2: Display Basic Information

```python
print(df.head())
print(df.info())
print(df.shape)
```

### Step 3: Check Missing Values

```python
print(df.isnull().sum())
```

### Step 4: Generate Summary Statistics

```python
print(df.describe())
```

### Step 5: Count Churned vs Active Customers

```python
print(df["Churn"].value_counts())
```

### Step 6: Average Spend by Churn Status

```python
print(df.groupby("Churn")["TotalSpend"].mean())
```

### Step 7: Visualize Churn Distribution

```python
import matplotlib.pyplot as plt

df["Churn"].value_counts().plot(kind="bar")
plt.title("Customer Churn Distribution")
plt.xlabel("Churn (0 = Active, 1 = Churned)")
plt.ylabel("Number of Customers")
plt.show()
```

### Step 8: Save a Clean Copy

```python
df.to_csv("customer_churn_clean.csv", index=False)
```

---

## Module Summary

* Use Python fundamentals with real customer churn examples.
* Apply variables, operators, conditions, loops, functions, modules, lists, and dictionaries to business problems.
* Handle errors and work safely with files.
* Create isolated Python environments and manage dependencies with `pip`.
* Use **NumPy** for numerical operations.
* Use **Pandas** to load, inspect, clean, filter, and summarize customer data.
* Create basic visualizations using **Matplotlib** to understand churn patterns.
* Read from and write to CSV files.
* Complete an exploratory analysis of the e-commerce customer churn dataset, preparing it for subsequent feature engineering and model development.
