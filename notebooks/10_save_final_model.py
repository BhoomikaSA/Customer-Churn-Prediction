# ============================================
# Customer Churn Prediction
# Stage 10: Save Final Trained Model Pipeline
# ============================================

import os
import json
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier

# ============================================
# STEP 1: Load and Clean Dataset
# ============================================

DATA_PATH = "data/raw/Telco-Customer-Churn.csv"
df = pd.read_csv(DATA_PATH)

df = df.drop(columns=["customerID"])
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
df = df.dropna(subset=["TotalCharges"])
df["Churn"] = df["Churn"].map({"No": 0, "Yes": 1})

X = df.drop(columns=["Churn"])
y = df["Churn"]

# Train / Test split for reference metadata
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    stratify=y,
    random_state=42
)

numerical_features = X.select_dtypes(include=["int64", "float64"]).columns.tolist()
categorical_features = X.select_dtypes(include=["str", "object"]).columns.tolist()

# ============================================
# STEP 2: Define Optimal Preprocessor & Pipeline
# ============================================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore", drop="first"),
            categorical_features
        ),
        (
            "numerical",
            StandardScaler(),
            numerical_features
        )
    ]
)

# Best Random Forest model hyperparameters from Stage 8 & 9
final_model = RandomForestClassifier(
    n_estimators=200,
    max_depth=8,
    min_samples_split=5,
    min_samples_leaf=1,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)

final_pipeline = Pipeline(
    steps=[
        ("preprocessing", preprocessor),
        ("classifier", final_model)
    ]
)

# ============================================
# STEP 3: Fit Final Pipeline on Full Data
# ============================================

print("=" * 70)
print("STAGE 10: SAVING FINAL MODEL PIPELINE")
print("=" * 70)

print("\nFitting final model pipeline on entire dataset...")
final_pipeline.fit(X, y)

# Ensure models directory exists
os.makedirs("models", exist_ok=True)

# Save Pipeline artifact
MODEL_PATH = "models/best_model_pipeline.joblib"
joblib.dump(final_pipeline, MODEL_PATH)
print(f"[OK] Saved trained pipeline artifact to: {MODEL_PATH}")

# Save Metadata JSON
metadata = {
    "model_type": "RandomForestClassifier",
    "target": "Churn",
    "numerical_features": numerical_features,
    "categorical_features": categorical_features,
    "best_parameters": {
        "n_estimators": 200,
        "max_depth": 8,
        "min_samples_split": 5,
        "min_samples_leaf": 1,
        "class_weight": "balanced"
    },
    "test_metrics": {
        "Accuracy": 0.7399,
        "Precision": 0.5067,
        "Recall": 0.8128,
        "F1": 0.6242,
        "ROC-AUC": 0.8383
    }
}

METADATA_PATH = "models/model_metadata.json"
with open(METADATA_PATH, "w") as f:
    json.dump(metadata, f, indent=4)

print(f"[OK] Saved metadata file to: {METADATA_PATH}")

# ============================================
# STEP 4: Verification - Load and Test Artifact
# ============================================

print("\n" + "=" * 70)
print("VERIFYING SAVED MODEL ARTIFACT")
print("=" * 70)

loaded_pipeline = joblib.load(MODEL_PATH)

# Test single sample prediction
sample_input = X.iloc[[0]]
prediction = loaded_pipeline.predict(sample_input)[0]
probability = loaded_pipeline.predict_proba(sample_input)[0][1]

churn_label = "Yes" if prediction == 1 else "No"
print(f"\nSample Input Customer:\n{sample_input.to_dict(orient='records')[0]}")
print(f"\nModel Output -> Predicted Churn: {churn_label} (Churn Probability: {probability:.4f})")
print("\n[OK] Verification successful! Saved model is functional and ready for backend API deployment.")
