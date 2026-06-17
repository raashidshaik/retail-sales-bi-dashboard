"""
generate_data.py
----------------
Generates a realistic 50,000-row retail sales dataset and saves it as
data/raw_sales_data.csv for use in analysis.py.

Author: Raashid Shaik
"""

import pandas as pd
import numpy as np
import os
import random
from datetime import datetime, timedelta

# ── Reproducibility ──────────────────────────────────────────────────────────
np.random.seed(42)
random.seed(42)

# ── Constants ─────────────────────────────────────────────────────────────────
NUM_RECORDS = 50_000

REGIONS = ["North", "South", "East", "West", "Central"]
CATEGORIES = ["Electronics", "Clothing", "Furniture", "Groceries", "Sports", "Toys", "Books"]
PAYMENT_METHODS = ["Credit Card", "Debit Card", "Cash", "Online Transfer"]
CUSTOMER_SEGMENTS = ["Retail", "Wholesale", "Online"]

PRODUCTS = {
    "Electronics": ["Laptop", "Smartphone", "Tablet", "Headphones", "Smart TV"],
    "Clothing":    ["T-Shirt", "Jeans", "Jacket", "Dress", "Shoes"],
    "Furniture":   ["Sofa", "Dining Table", "Bookshelf", "Office Chair", "Bed Frame"],
    "Groceries":   ["Rice Bag", "Cooking Oil", "Cereal Box", "Pasta Pack", "Juice Carton"],
    "Sports":      ["Running Shoes", "Yoga Mat", "Dumbbells", "Tennis Racket", "Cycling Helmet"],
    "Toys":        ["LEGO Set", "Action Figure", "Board Game", "Remote Car", "Puzzle"],
    "Books":       ["Fiction Novel", "Textbook", "Self-Help Book", "Comic Book", "Cookbook"],
}

PRICE_RANGES = {
    "Electronics": (150, 1500),
    "Clothing":    (20, 200),
    "Furniture":   (100, 1200),
    "Groceries":   (5, 50),
    "Sports":      (25, 300),
    "Toys":        (10, 120),
    "Books":       (8, 60),
}

# ── Date range: Jan 2022 – Dec 2024 ──────────────────────────────────────────
START_DATE = datetime(2022, 1, 1)
END_DATE   = datetime(2024, 12, 31)
DATE_RANGE = (END_DATE - START_DATE).days


def random_date():
    return START_DATE + timedelta(days=random.randint(0, DATE_RANGE))


def generate_dataset(n: int = NUM_RECORDS) -> pd.DataFrame:
    records = []
    for i in range(1, n + 1):
        category    = random.choice(CATEGORIES)
        product     = random.choice(PRODUCTS[category])
        unit_price  = round(random.uniform(*PRICE_RANGES[category]), 2)
        quantity    = random.randint(1, 10)
        discount    = round(random.choice([0, 0, 0, 0.05, 0.10, 0.15, 0.20]), 2)
        revenue     = round(unit_price * quantity * (1 - discount), 2)
        sale_date   = random_date()
        region      = random.choice(REGIONS)
        segment     = random.choice(CUSTOMER_SEGMENTS)
        payment     = random.choice(PAYMENT_METHODS)
        customer_id = f"CUST-{random.randint(1000, 9999)}"
        store_id    = f"STORE-{region[:1]}{random.randint(1, 20):02d}"

        # Inject ~3% dirty data for realism
        if random.random() < 0.03:
            revenue    = None        # missing revenue
        if random.random() < 0.01:
            unit_price = -unit_price  # negative price (data error)
        if random.random() < 0.005:
            region     = None        # missing region

        records.append({
            "transaction_id":   f"TXN-{i:06d}",
            "sale_date":        sale_date.strftime("%Y-%m-%d"),
            "customer_id":      customer_id,
            "store_id":         store_id,
            "region":           region,
            "customer_segment": segment,
            "category":         category,
            "product_name":     product,
            "unit_price":       unit_price,
            "quantity":         quantity,
            "discount":         discount,
            "revenue":          revenue,
            "payment_method":   payment,
        })

    return pd.DataFrame(records)


def main():
    os.makedirs("data", exist_ok=True)
    print("Generating 50,000-row retail sales dataset...")
    df = generate_dataset()
    output_path = "data/raw_sales_data.csv"
    df.to_csv(output_path, index=False)
    print(f"Dataset saved to {output_path}")
    print(f"Shape: {df.shape}")
    print(f"\nSample:\n{df.head(3).to_string()}")


if __name__ == "__main__":
    main()
