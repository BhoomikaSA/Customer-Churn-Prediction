# ============================================
# Customer Churn Prediction - EDA
# Stage 2: Exploratory Data Analysis
# ============================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
DATA_PATH = "data/raw/Telco-Customer-Churn.csv"

df = pd.read_csv(DATA_PATH)

print("=" * 70)
print("STAGE 2: EXPLORATORY DATA ANALYSIS")
print("=" * 70)

print("\nDataset shape:")
print(df.shape)

print("\nFirst 5 rows:")
print(df.head())

print("\nTotalCharges data type:")
print(df["TotalCharges"].dtype)

print("\nBlank TotalCharges values:")
print((df["TotalCharges"].str.strip() == "").sum())
df["TotalCharges"] = pd.to_numeric(
    df["TotalCharges"],
    errors="coerce"
)

print("\nTotalCharges after conversion:")
print(df["TotalCharges"].dtype)

print("\nMissing TotalCharges after conversion:")
print(df["TotalCharges"].isna().sum())
plt.figure(figsize=(7, 5))

sns.countplot(data=df, x="Churn")

plt.title("Customer Churn Distribution")
plt.xlabel("Churn")
plt.ylabel("Number of Customers")

plt.show()

# ============================================
# Contract Type vs Churn
# ============================================

print("\nChurn rate by Contract:")

churn_by_contract = pd.crosstab(
    df["Contract"],
    df["Churn"],
    normalize="index"
) * 100

print(churn_by_contract)

plt.figure(figsize=(8, 5))

sns.countplot(
    data=df,
    x="Contract",
    hue="Churn"
)

plt.title("Customer Churn by Contract Type")
plt.xlabel("Contract Type")
plt.ylabel("Number of Customers")

plt.tight_layout()
plt.show()

# ============================================
# Tenure vs Churn
# ============================================

plt.figure(figsize=(9, 5))

sns.boxplot(
    data=df,
    x="Churn",
    y="tenure"
)

plt.title("Customer Tenure by Churn Status")
plt.xlabel("Churn")
plt.ylabel("Tenure (Months)")

plt.tight_layout()
plt.show()

# ============================================
# Monthly Charges vs Churn
# ============================================

plt.figure(figsize=(9, 5))

sns.boxplot(
    data=df,
    x="Churn",
    y="MonthlyCharges"
)

plt.title("Monthly Charges by Churn Status")
plt.xlabel("Churn")
plt.ylabel("Monthly Charges")

plt.tight_layout()
plt.show()

# ============================================
# Monthly Charges Distribution
# ============================================

plt.figure(figsize=(9, 5))

sns.histplot(
    data=df,
    x="MonthlyCharges",
    hue="Churn",
    bins=30,
    kde=True
)

plt.title("Monthly Charges Distribution by Churn")
plt.xlabel("Monthly Charges")
plt.ylabel("Number of Customers")

plt.tight_layout()
plt.show()

# ============================================
# Categorical Features vs Churn
# ============================================

categorical_features = [
    "InternetService",
    "PaymentMethod",
    "TechSupport",
    "OnlineSecurity"
]

for feature in categorical_features:

    plt.figure(figsize=(9, 5))

    sns.countplot(
        data=df,
        x=feature,
        hue="Churn"
    )

    plt.title(f"{feature} vs Churn")
    plt.xlabel(feature)
    plt.ylabel("Number of Customers")

    plt.xticks(rotation=20)
    plt.tight_layout()
    plt.show()

    # ============================================
# Churn Rate by Categorical Features
# ============================================

for feature in categorical_features:

    churn_rate = pd.crosstab(
        df[feature],
        df["Churn"],
        normalize="index"
    ) * 100

    print("\n" + "=" * 60)
    print(f"Churn Rate by {feature}")
    print("=" * 60)

    print(churn_rate.round(2))

    # ============================================
# Numerical Feature Correlation
# ============================================

numerical_features = [
    "SeniorCitizen",
    "tenure",
    "MonthlyCharges",
    "TotalCharges"
]

correlation_matrix = df[numerical_features].corr()

print("\n" + "=" * 60)
print("CORRELATION MATRIX")
print("=" * 60)

print(correlation_matrix.round(2))

plt.figure(figsize=(8, 6))

sns.heatmap(
    correlation_matrix,
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)

plt.title("Numerical Feature Correlation")

plt.tight_layout()
plt.show()