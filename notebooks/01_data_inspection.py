# =============================================================================
# Stage 1: Data Inspection
# =============================================================================
# 
# PURPOSE:
#   This script loads the raw dataset and inspects it WITHOUT making any 
#   changes. Think of it as "looking at the data with a magnifying glass."
#
# WHAT YOU'LL LEARN:
#   - How to load a CSV file using pandas
#   - How to check the shape (rows x columns) of a dataset
#   - How to identify column names and data types
#   - How to find missing values
#   - How to detect duplicate rows
#   - How to separate categorical vs numerical features
#   - How to identify the target column
#
# IMPORTANT:
#   We NEVER modify the original dataset in this step. We only OBSERVE.
# =============================================================================

import pandas as pd
import numpy as np

# =============================================================================
# STEP 1: Load the Dataset
# =============================================================================
# pd.read_csv() reads a CSV (Comma-Separated Values) file into a DataFrame.
# A DataFrame is like a spreadsheet/table in Python -- it has rows and columns.

print("=" * 70)
print("STEP 1: Loading the Dataset")
print("=" * 70)

# Load the raw dataset (we never modify this file!)
df = pd.read_csv("data/raw/Telco-Customer-Churn.csv")

print("[OK] Dataset loaded successfully!")
print("   File: data/raw/Telco-Customer-Churn.csv")

# =============================================================================
# STEP 2: Check the Shape (Size) of the Dataset
# =============================================================================
# .shape returns (number_of_rows, number_of_columns)
# Rows = individual customers | Columns = features/attributes about each customer

print("\n" + "=" * 70)
print("STEP 2: Dataset Shape")
print("=" * 70)

rows, cols = df.shape
print(f"   Rows (customers):  {rows}")
print(f"   Columns (features): {cols}")
print(f"   Total data points:  {rows * cols}")

# =============================================================================
# STEP 3: Preview the Data (First and Last Rows)
# =============================================================================
# .head(n) shows the first n rows | .tail(n) shows the last n rows
# This helps us get a "feel" for what the data looks like.

print("\n" + "=" * 70)
print("STEP 3: Preview -- First 5 Rows")
print("=" * 70)
print(df.head(5).to_string())

print("\n" + "-" * 70)
print("Preview -- Last 5 Rows")
print("-" * 70)
print(df.tail(5).to_string())

# =============================================================================
# STEP 4: Column Names and Data Types
# =============================================================================
# Each column has a "data type" (dtype):
#   - object  = text/string (like names, categories)
#   - int64   = whole numbers (like age, tenure)
#   - float64 = decimal numbers (like charges)
#
# Understanding data types helps us know how to process each column later.

print("\n" + "=" * 70)
print("STEP 4: Column Names and Data Types")
print("=" * 70)

print(f"\n{'Column Name':<25} {'Data Type':<15} {'Example Value'}")
print("-" * 65)

for col in df.columns:
    dtype = str(df[col].dtype)
    example = str(df[col].iloc[0])  # First value as example
    print(f"{col:<25} {dtype:<15} {example}")

# =============================================================================
# STEP 5: Detailed Info (like a medical checkup for your data)
# =============================================================================
# .info() shows each column's name, how many non-null (non-empty) values 
# it has, and its data type. This is great for spotting columns with 
# missing data.

print("\n" + "=" * 70)
print("STEP 5: Dataset Info (Medical Checkup)")
print("=" * 70)
df.info()

# =============================================================================
# STEP 6: Statistical Summary of Numerical Columns
# =============================================================================
# .describe() gives us key statistics for numerical columns:
#   - count: how many non-null values
#   - mean:  the average
#   - std:   standard deviation (how spread out the values are)
#   - min:   smallest value
#   - 25%:   first quartile (25% of values are below this)
#   - 50%:   median (middle value)
#   - 75%:   third quartile
#   - max:   largest value

print("\n" + "=" * 70)
print("STEP 6: Statistical Summary (Numerical Columns)")
print("=" * 70)
print(df.describe().to_string())

# =============================================================================
# STEP 7: Statistical Summary of Categorical Columns
# =============================================================================
# For text/category columns, describe() shows:
#   - count:  how many non-null values
#   - unique: how many distinct categories
#   - top:    the most frequent category
#   - freq:   how many times the top category appears

print("\n" + "=" * 70)
print("STEP 7: Statistical Summary (Categorical Columns)")
print("=" * 70)
print(df.describe(include='object').to_string())

# =============================================================================
# STEP 8: Missing Values Analysis
# =============================================================================
# Missing values (NaN/null) are empty cells in the data.
# ML models usually can't handle missing values, so we need to know 
# WHERE and HOW MANY are missing before we decide how to fix them.

print("\n" + "=" * 70)
print("STEP 8: Missing Values Analysis")
print("=" * 70)

missing = df.isnull().sum()  # Count missing values per column
missing_pct = (df.isnull().sum() / len(df) * 100).round(2)  # Percentage

# Create a summary table
missing_table = pd.DataFrame({
    'Missing Count': missing,
    'Missing %': missing_pct
})

# Show only columns that have missing values (if any)
has_missing = missing_table[missing_table['Missing Count'] > 0]

if len(has_missing) > 0:
    print("\n[WARNING] Columns with missing values:")
    print(has_missing.to_string())
else:
    print("\n[OK] No missing values found as NaN! (But we should double-check...)")

# IMPORTANT: Sometimes missing values are hidden as empty strings " " or 
# special values. Let's check for those too.
print("\n[SEARCH] Checking for hidden missing values (empty strings, spaces)...")
for col in df.columns:
    if df[col].dtype == 'object':
        # Count empty strings and whitespace-only values
        empty_count = (df[col].str.strip() == '').sum()
        if empty_count > 0:
            print(f"   [WARNING] '{col}' has {empty_count} empty string values!")

# =============================================================================
# STEP 9: Duplicate Rows
# =============================================================================
# Duplicate rows mean the exact same customer appears more than once.
# This can skew our model because it gives extra weight to duplicated data.

print("\n" + "=" * 70)
print("STEP 9: Duplicate Rows Check")
print("=" * 70)

duplicates = df.duplicated().sum()
print(f"   Number of duplicate rows: {duplicates}")

if duplicates > 0:
    print(f"   [WARNING] Found {duplicates} duplicate rows! We'll handle these in Stage 3.")
else:
    print(f"   [OK] No duplicate rows found!")

# Also check if customerID column has duplicates (should be unique per customer)
if 'customerID' in df.columns:
    id_duplicates = df['customerID'].duplicated().sum()
    print(f"   Duplicate customerIDs: {id_duplicates}")

# =============================================================================
# STEP 10: Identify Categorical vs Numerical Features
# =============================================================================
# This is crucial for ML because:
#   - Categorical features (text) need to be ENCODED into numbers
#   - Numerical features may need to be SCALED (normalized)

print("\n" + "=" * 70)
print("STEP 10: Feature Classification")
print("=" * 70)

# Separate columns by data type
categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()

print(f"\n[CATEGORICAL] Categorical Features ({len(categorical_cols)}):")
for i, col in enumerate(categorical_cols, 1):
    unique_count = df[col].nunique()
    print(f"   {i}. {col:<25} -> {unique_count} unique values")

print(f"\n[NUMERICAL] Numerical Features ({len(numerical_cols)}):")
for i, col in enumerate(numerical_cols, 1):
    print(f"   {i}. {col:<25} -> min={df[col].min()}, max={df[col].max()}")

# =============================================================================
# STEP 11: Target Column Analysis
# =============================================================================
# The TARGET column is what we want to PREDICT. In our case, it's "Churn".
# We need to check:
#   - What values it has (Yes/No)
#   - Is it balanced? (roughly equal Yes and No?)
# 
# CLASS IMBALANCE: If one class vastly outnumbers the other, the model 
# might just predict the majority class every time and still look "accurate".

print("\n" + "=" * 70)
print("STEP 11: Target Column -- 'Churn'")
print("=" * 70)

if 'Churn' in df.columns:
    print(f"\n   Unique values: {df['Churn'].unique()}")
    print(f"\n   Value counts:")
    churn_counts = df['Churn'].value_counts()
    for value, count in churn_counts.items():
        pct = (count / len(df) * 100)
        bar = "#" * int(pct / 2)  # Visual bar
        print(f"   {value:>5}: {count:>5} ({pct:.1f}%) {bar}")
    
    # Calculate imbalance ratio
    majority = churn_counts.max()
    minority = churn_counts.min()
    ratio = majority / minority
    print(f"\n   Imbalance ratio: {ratio:.2f}:1")
    
    if ratio > 5:
        print("   [ALERT] Severe class imbalance! Will need special handling.")
    elif ratio > 2:
        print("   [WARNING] Moderate class imbalance detected! We'll address this later.")
    else:
        print("   [OK] Classes are reasonably balanced.")
else:
    print("   [ERROR] 'Churn' column not found! Check column names.")

# =============================================================================
# STEP 12: Unique Values Per Column (Quick Overview)
# =============================================================================
# This helps us understand the "cardinality" of each feature.
# Low cardinality (few unique values) -> likely categorical
# High cardinality (many unique values) -> likely numerical or ID column

print("\n" + "=" * 70)
print("STEP 12: Unique Values Per Column")
print("=" * 70)

print(f"\n{'Column':<25} {'Unique Values':<15} {'Sample Values'}")
print("-" * 75)

for col in df.columns:
    unique_count = df[col].nunique()
    sample = df[col].unique()[:4]  # Show first 4 unique values
    sample_str = str(list(sample))
    if len(sample_str) > 40:
        sample_str = sample_str[:40] + "..."
    print(f"{col:<25} {unique_count:<15} {sample_str}")

# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 70)
print("STAGE 1 SUMMARY")
print("=" * 70)
print(f"""
   Dataset:              Telco Customer Churn
   Total Rows:           {rows}
   Total Columns:        {cols}
   Categorical Features: {len(categorical_cols)}
   Numerical Features:   {len(numerical_cols)}
   Missing Values:       {df.isnull().sum().sum()} (explicit NaN)
   Duplicate Rows:       {duplicates}
   Target Column:        Churn
   
   [OK] Data inspection complete!
   --> Next: Stage 2 -- Exploratory Data Analysis (EDA)
""")
