# ============================================
# Customer Churn Prediction
# Stage 9: Final Model Evaluation on Unseen Test Set
# ============================================

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)

# ============================================
# STEP 1: Load and Clean Dataset
# ============================================

DATA_PATH = "data/raw/Telco-Customer-Churn.csv"
df = pd.read_csv(DATA_PATH)

df = df.drop(columns=["customerID"])
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
df = df.dropna(subset=["TotalCharges"])
df["Churn"] = df["Churn"].map({"No": 0, "Yes": 1})

# ============================================
# STEP 2: Train / Test Split (Holdout Test Set)
# ============================================

X = df.drop(columns=["Churn"])
y = df["Churn"]

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
# STEP 3: Preprocessor Setup
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

# ============================================
# STEP 4: Define Tuned Models
# ============================================

tuned_models = {
    "Logistic Regression (Tuned)": LogisticRegression(
        C=0.1,
        class_weight="balanced",
        max_iter=1000,
        random_state=42
    ),

    "Random Forest (Tuned)": RandomForestClassifier(
        n_estimators=200,
        max_depth=8,
        min_samples_split=5,
        min_samples_leaf=1,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    ),

    "XGBoost (Tuned)": XGBClassifier(
        n_estimators=200,
        max_depth=3,
        learning_rate=0.1,
        subsample=0.7,
        colsample_bytree=0.7,
        random_state=42,
        eval_metric="logloss",
        n_jobs=-1
    )
}

# ============================================
# STEP 5: Train and Evaluate on Test Set
# ============================================

print("=" * 70)
print("STAGE 9: FINAL MODEL EVALUATION ON UNSEEN TEST SET")
print("=" * 70)

results = []

for name, model in tuned_models.items():
    print(f"\n--- Evaluating {name} ---")
    
    pipeline = Pipeline(
        steps=[
            ("preprocessing", preprocessor),
            ("classifier", model)
        ]
    )

    # Train on training set
    pipeline.fit(X_train, y_train)

    # Predict on test set
    y_pred = pipeline.predict(X_test)
    y_proba = pipeline.predict_proba(X_test)[:, 1]

    # Metrics
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_proba)

    results.append({
        "Model": name,
        "Accuracy": acc,
        "Precision": prec,
        "Recall": rec,
        "F1": f1,
        "ROC-AUC": auc
    })

    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=["No Churn", "Churn"]))

# ============================================
# STEP 6: Final Comparison Table
# ============================================

results_df = pd.DataFrame(results)

print("\n" + "=" * 70)
print("FINAL TEST SET PERFORMANCE SUMMARY")
print("=" * 70)

print(
    results_df.to_string(
        index=False,
        float_format=lambda x: f"{x:.4f}"
    )
)
