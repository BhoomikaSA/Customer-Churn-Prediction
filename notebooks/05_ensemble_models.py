# ============================================
# Customer Churn Prediction
# Stage 5: Tree & Ensemble Models
# ============================================

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier

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
# STEP 2: Features and Target
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
# STEP 3: Train-Test Split
# ============================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)
# ============================================
# STEP 4: Preprocessing
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
# STEP 5: Random Forest
# ============================================

model = Pipeline(
    steps=[
        ("preprocessing", preprocessor),
        (
            "classifier",
            RandomForestClassifier(
                n_estimators=200,
                max_depth=8,
                random_state=42,
                n_jobs=-1
            )
        )
    ]
)

# ============================================
# STEP 6: Train
# ============================================

print("=" * 70)
print("RANDOM FOREST")
print("=" * 70)

print("\nTraining Random Forest...")
model.fit(X_train, y_train)

print("[OK] Training completed!")

# ============================================
# STEP 7: Evaluation
# ============================================

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("\nAccuracy:")
print(f"{accuracy:.4f}")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

