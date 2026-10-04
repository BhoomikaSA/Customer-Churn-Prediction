# ============================================
# Customer Churn Prediction
# Stage 6: XGBoost
# ============================================

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline

from xgboost import XGBClassifier

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)
# ============================================
# STEP 1: Load Dataset
# ============================================

DATA_PATH = "data/raw/Telco-Customer-Churn.csv"

df = pd.read_csv(DATA_PATH)

print("=" * 70)
print("STAGE 6: XGBOOST")
print("=" * 70)

print("\nOriginal dataset:")
print(df.shape)
# ============================================
# STEP 2: Data Cleaning
# ============================================

df = df.drop(columns=["customerID"])

df["TotalCharges"] = pd.to_numeric(
    df["TotalCharges"],
    errors="coerce"
)

df = df.dropna(subset=["TotalCharges"])

df["Churn"] = df["Churn"].map({
    "No": 0,
    "Yes": 1
})
# ============================================
# STEP 3: Features and Target
# ============================================

X = df.drop(columns=["Churn"])
y = df["Churn"]

numerical_features = X.select_dtypes(
    include=["int64", "float64"]
).columns.tolist()

categorical_features = X.select_dtypes(
    include=["str"]
).columns.tolist()
# ============================================
# STEP 4: Train-Test Split
# ============================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)
# ============================================
# STEP 5: Preprocessing
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
# ============================================
# STEP 6: Handle Class Imbalance
# ============================================

negative = (y_train == 0).sum()
positive = (y_train == 1).sum()

scale_pos_weight = negative / positive

print("\nClass imbalance:")
print(f"Non-churn customers: {negative}")
print(f"Churn customers:     {positive}")
print(f"Scale pos weight:    {scale_pos_weight:.2f}")

# ============================================
# STEP 7: XGBoost Model
# ============================================

model = Pipeline(
    steps=[
        ("preprocessing", preprocessor),
        (
            "classifier",
            XGBClassifier(
                n_estimators=200,
                max_depth=4,
                learning_rate=0.05,
                subsample=0.8,
                colsample_bytree=0.8,
                scale_pos_weight=scale_pos_weight,
                random_state=42,
                eval_metric="logloss",
                n_jobs=-1
            )
        )
    ]
)
# ============================================
# STEP 8: Train XGBoost
# ============================================

print("\nTraining XGBoost...")

model.fit(X_train, y_train)

print("[OK] XGBoost training completed!")
# ============================================
# STEP 9: Predictions
# ============================================

y_pred = model.predict(X_test)
# ============================================
# STEP 10: Evaluation
# ============================================

accuracy = accuracy_score(y_test, y_pred)

print("\n" + "=" * 70)
print("XGBOOST RESULTS")
print("=" * 70)

print(f"\nAccuracy: {accuracy:.4f}")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))