"""
analysis.py
-----------
Full data cleaning, transformation, and exploratory data analysis (EDA)
pipeline for the retail sales dataset.

Outputs:
  - data/cleaned_sales_data.csv   : cleaned, analysis-ready dataset
  - data/summary_report.txt       : key findings summary

Author: Raashid Shaik
"""

import pandas as pd
import numpy as np
import os

# ── Configuration ─────────────────────────────────────────────────────────────
RAW_DATA_PATH     = "data/raw_sales_data.csv"
CLEANED_DATA_PATH = "data/cleaned_sales_data.csv"
REPORT_PATH       = "data/summary_report.txt"


# ─────────────────────────────────────────────────────────────────────────────
# 1. LOAD DATA
# ─────────────────────────────────────────────────────────────────────────────
def load_data(path: str) -> pd.DataFrame:
    """Load raw CSV into a DataFrame."""
    print("=" * 60)
    print("STEP 1: Loading Data")
    print("=" * 60)
    df = pd.read_csv(path, parse_dates=["sale_date"])
    print(f"  Rows loaded    : {len(df):,}")
    print(f"  Columns        : {list(df.columns)}")
    print(f"  Date range     : {df['sale_date'].min()} → {df['sale_date'].max()}")
    return df


# ─────────────────────────────────────────────────────────────────────────────
# 2. DATA QUALITY AUDIT
# ─────────────────────────────────────────────────────────────────────────────
def audit_quality(df: pd.DataFrame) -> dict:
    """Identify missing values, duplicates, and anomalies."""
    print("\n" + "=" * 60)
    print("STEP 2: Data Quality Audit")
    print("=" * 60)

    issues = {}

    # Missing values
    missing = df.isnull().sum()
    missing = missing[missing > 0]
    issues["missing"] = missing.to_dict()
    print(f"\n  Missing values:\n{missing.to_string()}")

    # Duplicates
    dupes = df.duplicated(subset="transaction_id").sum()
    issues["duplicates"] = dupes
    print(f"\n  Duplicate transaction IDs: {dupes}")

    # Negative prices
    neg_price = (df["unit_price"] < 0).sum()
    issues["negative_prices"] = neg_price
    print(f"  Negative unit prices     : {neg_price}")

    # Zero quantity
    zero_qty = (df["quantity"] <= 0).sum()
    issues["zero_quantity"] = zero_qty
    print(f"  Zero/negative quantities : {zero_qty}")

    return issues


# ─────────────────────────────────────────────────────────────────────────────
# 3. DATA CLEANING
# ─────────────────────────────────────────────────────────────────────────────
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Apply cleaning rules and return a clean DataFrame."""
    print("\n" + "=" * 60)
    print("STEP 3: Data Cleaning")
    print("=" * 60)
    original_len = len(df)

    # Fix negative unit prices
    df["unit_price"] = df["unit_price"].abs()
    print("  ✓ Converted negative unit prices to absolute values")

    # Recalculate revenue where missing or inconsistent
    df["revenue"] = df["unit_price"] * df["quantity"] * (1 - df["discount"])
    df["revenue"] = df["revenue"].round(2)
    print("  ✓ Recalculated revenue: unit_price × quantity × (1 - discount)")

    # Fill missing region with mode
    mode_region = df["region"].mode()[0]
    df["region"] = df["region"].fillna(mode_region)
    print(f"  ✓ Filled missing region values with mode: '{mode_region}'")

    # Drop duplicate transaction IDs (keep first)
    df = df.drop_duplicates(subset="transaction_id", keep="first")
    print(f"  ✓ Removed duplicates: {original_len - len(df)} rows dropped")

    # Drop rows with zero or negative quantity
    df = df[df["quantity"] > 0]

    # Standardize column types
    df["sale_date"]        = pd.to_datetime(df["sale_date"])
    df["transaction_id"]   = df["transaction_id"].astype(str)
    df["customer_segment"] = df["customer_segment"].str.strip().str.title()
    df["category"]         = df["category"].str.strip().str.title()
    df["region"]           = df["region"].str.strip().str.title()

    # Derived columns
    df["year"]    = df["sale_date"].dt.year
    df["month"]   = df["sale_date"].dt.month
    df["quarter"] = df["sale_date"].dt.quarter
    df["month_name"] = df["sale_date"].dt.strftime("%b")

    print(f"  ✓ Added derived columns: year, month, quarter, month_name")
    print(f"\n  Final clean dataset: {len(df):,} rows × {len(df.columns)} columns")
    return df


# ─────────────────────────────────────────────────────────────────────────────
# 4. EXPLORATORY DATA ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
def run_eda(df: pd.DataFrame) -> dict:
    """Compute key business metrics and return findings dict."""
    print("\n" + "=" * 60)
    print("STEP 4: Exploratory Data Analysis")
    print("=" * 60)

    findings = {}

    # ── Overall KPIs ──────────────────────────────────────────────────────────
    total_revenue     = df["revenue"].sum()
    total_orders      = len(df)
    avg_order_value   = df["revenue"].mean()
    total_units_sold  = df["quantity"].sum()

    findings["total_revenue"]    = round(total_revenue, 2)
    findings["total_orders"]     = total_orders
    findings["avg_order_value"]  = round(avg_order_value, 2)
    findings["total_units_sold"] = int(total_units_sold)

    print(f"\n  📊 Overall KPIs:")
    print(f"     Total Revenue    : ${total_revenue:,.2f}")
    print(f"     Total Orders     : {total_orders:,}")
    print(f"     Avg Order Value  : ${avg_order_value:,.2f}")
    print(f"     Total Units Sold : {total_units_sold:,}")

    # ── Revenue by Region ─────────────────────────────────────────────────────
    region_revenue = (
        df.groupby("region")["revenue"]
        .sum()
        .sort_values(ascending=False)
        .round(2)
    )
    findings["revenue_by_region"] = region_revenue.to_dict()
    print(f"\n  🗺️  Revenue by Region:")
    for region, rev in region_revenue.items():
        print(f"     {region:<10}: ${rev:>15,.2f}")

    # ── Revenue by Category ───────────────────────────────────────────────────
    category_revenue = (
        df.groupby("category")["revenue"]
        .sum()
        .sort_values(ascending=False)
        .round(2)
    )
    findings["revenue_by_category"] = category_revenue.to_dict()
    print(f"\n  🏷️  Revenue by Category:")
    for cat, rev in category_revenue.items():
        print(f"     {cat:<15}: ${rev:>15,.2f}")

    # ── Monthly Revenue Trend ─────────────────────────────────────────────────
    monthly_trend = (
        df.groupby(["year", "month"])["revenue"]
        .sum()
        .round(2)
        .reset_index()
        .sort_values(["year", "month"])
    )
    findings["monthly_trend_rows"] = len(monthly_trend)
    print(f"\n  📈 Monthly Revenue Trend: {len(monthly_trend)} data points computed")

    # ── Customer Segment Analysis ─────────────────────────────────────────────
    segment_analysis = (
        df.groupby("customer_segment")
        .agg(
            total_revenue=("revenue", "sum"),
            total_orders=("transaction_id", "count"),
            avg_order_value=("revenue", "mean"),
        )
        .round(2)
        .sort_values("total_revenue", ascending=False)
    )
    findings["segment_analysis"] = segment_analysis.to_dict()
    print(f"\n  👥 Customer Segment Analysis:")
    print(segment_analysis.to_string())

    # ── Discount Impact ───────────────────────────────────────────────────────
    discount_impact = (
        df.groupby("discount")
        .agg(avg_revenue=("revenue", "mean"), count=("transaction_id", "count"))
        .round(2)
    )
    findings["discount_levels"] = len(discount_impact)
    print(f"\n  💰 Discount Levels Analyzed: {len(discount_impact)}")

    # ── Top 5 Products by Revenue ─────────────────────────────────────────────
    top_products = (
        df.groupby("product_name")["revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .round(2)
    )
    findings["top_products"] = top_products.to_dict()
    print(f"\n  🏆 Top 5 Products by Revenue:")
    for prod, rev in top_products.items():
        print(f"     {prod:<20}: ${rev:>15,.2f}")

    # ── Outlier Detection ─────────────────────────────────────────────────────
    Q1 = df["revenue"].quantile(0.25)
    Q3 = df["revenue"].quantile(0.75)
    IQR = Q3 - Q1
    outliers = df[(df["revenue"] < Q1 - 1.5 * IQR) | (df["revenue"] > Q3 + 1.5 * IQR)]
    findings["outlier_count"] = len(outliers)
    print(f"\n  ⚠️  Revenue Outliers Detected (IQR method): {len(outliers):,} rows")

    return findings


# ─────────────────────────────────────────────────────────────────────────────
# 5. GENERATE SUMMARY REPORT
# ─────────────────────────────────────────────────────────────────────────────
def generate_report(findings: dict, output_path: str):
    """Write a plain-text summary report of key findings."""
    lines = [
        "=" * 60,
        "RETAIL SALES ANALYSIS — SUMMARY REPORT",
        "=" * 60,
        "",
        "OVERALL KPIs",
        "-" * 40,
        f"Total Revenue    : ${findings['total_revenue']:,.2f}",
        f"Total Orders     : {findings['total_orders']:,}",
        f"Avg Order Value  : ${findings['avg_order_value']:,.2f}",
        f"Total Units Sold : {findings['total_units_sold']:,}",
        "",
        "REVENUE BY REGION",
        "-" * 40,
    ]
    for region, rev in findings["revenue_by_region"].items():
        lines.append(f"  {region:<10}: ${rev:>15,.2f}")

    lines += [
        "",
        "REVENUE BY CATEGORY",
        "-" * 40,
    ]
    for cat, rev in findings["revenue_by_category"].items():
        lines.append(f"  {cat:<15}: ${rev:>15,.2f}")

    lines += [
        "",
        "TOP 5 PRODUCTS BY REVENUE",
        "-" * 40,
    ]
    for prod, rev in findings["top_products"].items():
        lines.append(f"  {prod:<20}: ${rev:>15,.2f}")

    lines += [
        "",
        "DATA QUALITY",
        "-" * 40,
        f"Revenue Outliers Detected: {findings['outlier_count']:,}",
        f"Monthly Trend Periods    : {findings['monthly_trend_rows']}",
        "",
        "=" * 60,
        "Report generated by analysis.py",
        "=" * 60,
    ]

    with open(output_path, "w") as f:
        f.write("\n".join(lines))
    print(f"\n  ✓ Summary report saved to {output_path}")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────
def main():
    os.makedirs("data", exist_ok=True)

    df       = load_data(RAW_DATA_PATH)
    _        = audit_quality(df)
    df_clean = clean_data(df)
    findings = run_eda(df_clean)

    # Save cleaned data
    df_clean.to_csv(CLEANED_DATA_PATH, index=False)
    print(f"\n  ✓ Cleaned dataset saved to {CLEANED_DATA_PATH}")

    generate_report(findings, REPORT_PATH)

    print("\n" + "=" * 60)
    print("✅ Pipeline complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
