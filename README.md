# Retail Sales BI Dashboard — Data Analysis Pipeline

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458?logo=pandas)
![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-F2C811?logo=powerbi)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)

## 📌 Project Overview

An end-to-end data analysis pipeline built on a **50,000-row retail sales dataset**, covering data generation, cleaning, exploratory data analysis (EDA), and business intelligence reporting via Power BI.

This project demonstrates real-world data analyst skills: handling messy data, building ETL workflows, computing business KPIs, detecting outliers, and translating raw data into actionable insights for stakeholders.

---

## 🎯 Business Questions Answered

- Which regions generate the most revenue — and why?
- What product categories drive the highest sales volume?
- How do discounts affect average order value?
- What are the monthly and quarterly revenue trends over 3 years?
- Which customer segments (Retail, Wholesale, Online) are most valuable?

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.10+ | Core scripting language |
| Pandas | Data wrangling and transformation |
| NumPy | Numerical operations and outlier detection |
| Power BI | Interactive KPI dashboard (DAX, Power Query) |
| Git/GitHub | Version control |

---

## 📁 Project Structure

```
retail-sales-bi-dashboard/
│
├── data/
│   ├── raw_sales_data.csv          # Generated raw dataset (50K rows)
│   ├── cleaned_sales_data.csv      # Output of cleaning pipeline
│   └── summary_report.txt          # Auto-generated findings report
│
├── generate_data.py                # Generates realistic 50K row dataset
├── analysis.py                     # ETL + EDA pipeline
├── requirements.txt                # Python dependencies
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/raashid-shaik/retail-sales-bi-dashboard.git
cd retail-sales-bi-dashboard
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Generate the dataset
```bash
python generate_data.py
```

### 4. Run the analysis pipeline
```bash
python analysis.py
```

---

## 📊 Key Findings

| KPI | Value |
|---|---|
| Total Revenue (3 years) | ~$47.2M |
| Total Transactions | 50,000 |
| Average Order Value | ~$944 |
| Top Region | North |
| Top Category | Electronics |
| Outliers Detected | ~1,400 rows (IQR method) |

---

## 🔍 Pipeline Steps

### Step 1 — Data Generation
Simulates 3 years (2022–2024) of retail transactions across 5 regions, 7 categories, and 3 customer segments. Intentionally injects ~3% dirty data (missing values, negative prices) to mimic real-world data quality issues.

### Step 2 — Data Quality Audit
Identifies missing values, duplicate transaction IDs, negative unit prices, and zero-quantity orders before any transformation.

### Step 3 — Data Cleaning
- Corrects negative unit prices using absolute value conversion
- Recalculates revenue from source fields to fix missing values
- Fills missing region values with the statistical mode
- Removes duplicate records
- Adds derived time columns: `year`, `month`, `quarter`, `month_name`

### Step 4 — Exploratory Data Analysis
Computes revenue by region, category, customer segment, and product. Performs monthly trend analysis, discount impact analysis, and IQR-based outlier detection.

### Step 5 — Reporting
Outputs a plain-text summary report and a cleaned CSV ready for Power BI ingestion.

---

## 📈 Power BI Dashboard

The cleaned dataset (`data/cleaned_sales_data.csv`) feeds directly into a Power BI dashboard with:
- Revenue trend line chart (monthly/quarterly toggle)
- Regional performance map
- Category breakdown bar chart
- Customer segment comparison
- KPI cards: Total Revenue, Avg Order Value, Total Orders

---

## 👤 Author

**Raashid Shaik**
M.S. Management Information Systems — Lamar University (GPA 3.90)
📧 shaikraashid088@gmail.com
🔗 [LinkedIn](https://linkedin.com/in/raashid-shaik-53a3)
🐙 [GitHub](https://github.com/raashid-shaik)
