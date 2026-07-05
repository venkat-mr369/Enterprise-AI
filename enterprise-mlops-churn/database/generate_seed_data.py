"""
generate_seed_data.py
----------------------
Generates ~1000 synthetic customer records with Indian names, cities,
and states for Module 3-A, using the same churn feature schema as the
core ML pipeline (src/data_ingestion.py) so this data can later be
exported and fed straight into `python -m src.train`.

Usage:
    python generate_seed_data.py --count 1000 --out seed_customers.csv
"""

import argparse
import csv
import random

from faker import Faker

fake = Faker("en_IN")
Faker.seed(42)
random.seed(42)

INDIAN_STATE_CITY = {
    "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Nashik"],
    "Karnataka": ["Bengaluru", "Mysuru", "Mangaluru"],
    "Delhi": ["New Delhi", "Dwarka", "Rohini"],
    "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai"],
    "Telangana": ["Hyderabad", "Warangal"],
    "West Bengal": ["Kolkata", "Howrah", "Siliguri"],
    "Gujarat": ["Ahmedabad", "Surat", "Vadodara"],
    "Uttar Pradesh": ["Lucknow", "Noida", "Kanpur"],
    "Rajasthan": ["Jaipur", "Udaipur", "Jodhpur"],
    "Kerala": ["Kochi", "Thiruvananthapuram", "Kozhikode"],
    "Punjab": ["Chandigarh", "Ludhiana", "Amritsar"],
    "Haryana": ["Gurugram", "Faridabad"],
}

INTERNET_SERVICE = ["DSL", "Fiber optic", "No"]
CONTRACT = ["Month-to-month", "One year", "Two year"]
PAYMENT_METHOD = ["Electronic check", "Mailed check", "Bank transfer", "UPI", "Credit card"]
YES_NO = ["Yes", "No"]


def generate_record(i: int) -> dict:
    gender = random.choice(["Male", "Female"])
    full_name = fake.name_male() if gender == "Male" else fake.name_female()

    state = random.choice(list(INDIAN_STATE_CITY.keys()))
    city = random.choice(INDIAN_STATE_CITY[state])

    tenure = random.randint(0, 72)
    monthly_charges = round(random.uniform(299, 2999), 2)  # INR broadband-style pricing
    total_charges = round(monthly_charges * tenure + random.uniform(0, 500), 2)

    contract = random.choices(CONTRACT, weights=[0.55, 0.25, 0.20])[0]
    internet = random.choices(INTERNET_SERVICE, weights=[0.35, 0.45, 0.20])[0]
    senior = random.choices([0, 1], weights=[0.84, 0.16])[0]

    # Same churn-likelihood logic used in the core project's synthetic dataset,
    # so this data is statistically consistent with data/raw/customer_churn.csv
    score = (
        (contract == "Month-to-month") * 0.35
        + (internet == "Fiber optic") * 0.20
        - (tenure / 72) * 0.30
        + (monthly_charges / 2999) * 0.20
        + (senior == 1) * 0.05
        + random.gauss(0, 0.15)
    )
    churn = "Yes" if score > 0.15 else "No"
    if random.random() < 0.05:  # noise
        churn = "No" if churn == "Yes" else "Yes"

    return {
        "customer_id": f"IN-CUST-{i:05d}",
        "full_name": full_name,
        "gender": gender,
        "senior_citizen": senior,
        "partner": random.choice(YES_NO),
        "dependents": random.choice(YES_NO),
        "city": city,
        "state": state,
        "tenure_months": tenure,
        "internet_service": internet,
        "contract": contract,
        "paperless_billing": random.choice(YES_NO),
        "payment_method": random.choice(PAYMENT_METHOD),
        "monthly_charges_inr": monthly_charges,
        "total_charges_inr": total_charges,
        "churn": churn,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=1000)
    parser.add_argument("--out", type=str, default="seed_customers.csv")
    args = parser.parse_args()

    fieldnames = [
        "customer_id", "full_name", "gender", "senior_citizen", "partner",
        "dependents", "city", "state", "tenure_months", "internet_service",
        "contract", "paperless_billing", "payment_method",
        "monthly_charges_inr", "total_charges_inr", "churn",
    ]

    with open(args.out, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(1, args.count + 1):
            writer.writerow(generate_record(i))

    print(f"Wrote {args.count} records to {args.out}")


if __name__ == "__main__":
    main()
