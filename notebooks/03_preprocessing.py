# ============================================
# Customer Churn Prediction
# Stage 3: Data Preprocessing
# ============================================

import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

# Load dataset
DATA_PATH = "data/raw/Telco-Customer-Churn.csv"

df = pd.read_csv(DATA_PATH)

print("=" * 70)
print("STAGE 3: DATA PREPROCESSING")
print("=" * 70)

print("\nOriginal shape:")
print(df.shape)

print("\nOriginal data types:")
print(df.dtypes)

df = df.drop(columns=["customerID"])

print("\nAfter removing customerID:")
print(df.shape)
df["TotalCharges"] = pd.to_numeric(
    df["TotalCharges"],
    errors="coerce"
)

print("\nTotalCharges dtype:")
print(df["TotalCharges"].dtype)

print("\nMissing TotalCharges:")
print(df["TotalCharges"].isna().sum())

df = df.dropna(subset=["TotalCharges"])

print("\nShape after handling missing TotalCharges:")
print(df.shape)

df["Churn"] = df["Churn"].map({
    "No": 0,
    "Yes": 1
})

print("\nChurn values after encoding:")
print(df["Churn"].value_counts())
print("\n" + "=" * 70)
print("PREPROCESSING CHECK")
print("=" * 70)

print("\nShape:")
print(df.shape)

print("\nMissing values:")
print(df.isnull().sum())

print("\nData types:")
print(df.dtypes)
# ============================================
# Step 7: Separate Features and Target
# ============================================

X = df.drop(columns=["Churn"])
y = df["Churn"]

print("\n" + "=" * 70)
print("FEATURES AND TARGET")
print("=" * 70)

print("\nX shape:")
print(X.shape)

print("\ny shape:")
print(y.shape)

print("\nX columns:")
print(X.columns.tolist())

print("\ny distribution:")
print(y.value_counts())
# ============================================
# Step 8: Identify Feature Types
# ============================================

numerical_features = X.select_dtypes(
    include=["int64", "float64"]
).columns.tolist()

categorical_features = X.select_dtypes(
    include=["str"]
).columns.tolist()

print("\nNumerical features:")
print(numerical_features)

print("\nCategorical features:")
print(categorical_features)
# ============================================
# Step 9: Train-Test Split
# ============================================

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\n" + "=" * 70)
print("TRAIN-TEST SPLIT")
print("=" * 70)

print("\nTraining features:", X_train.shape)
print("Testing features:", X_test.shape)

print("\nTraining target:", y_train.shape)
print("Testing target:", y_test.shape)

print("\nTraining churn distribution:")
print(y_train.value_counts(normalize=True).round(3))

print("\nTesting churn distribution:")
print(y_test.value_counts(normalize=True).round(3))


# ============================================
# Step 10: Categorical Encoding
# ============================================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(
                handle_unknown="ignore",
                drop="first"
            ),
            categorical_features
        )
    ],
    remainder="passthrough"
)

print("\nPreprocessor created successfully!")
print("Categorical features will be One-Hot Encoded.")
print("Numerical features will be passed through.")
# ============================================
# Step 10: Encoding + Scaling
# ============================================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(
                handle_unknown="ignore",
                drop="first"
            ),
            categorical_features
        ),
        (
            "numerical",
            StandardScaler(),
            numerical_features
        )
    ]
)

print("\nPreprocessor created successfully!")
print("Categorical features → One-Hot Encoding")
print("Numerical features → StandardScaler")