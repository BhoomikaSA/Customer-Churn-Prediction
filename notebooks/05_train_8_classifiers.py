# ============================================
# Customer Churn Prediction
# Stage 5: Training 8 Classifiers
# ============================================

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split, cross_validate, StratifiedKFold
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline

# 8 Classifiers
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    RandomForestClassifier,
    GradientBoostingClassifier,
    AdaBoostClassifier,
    ExtraTreesClassifier
)
from sklearn.neighbors import KNeighborsClassifier
from xgboost import XGBClassifier

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
# STEP 2: Features and Target Split
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
# STEP 3: Preprocessor
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
# STEP 4: Define 8 Classifiers
# ============================================

classifiers = {
    "1. Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
    "2. Decision Tree": DecisionTreeClassifier(max_depth=5, random_state=42),
    "3. Random Forest": RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1),
    "4. Gradient Boosting": GradientBoostingClassifier(n_estimators=100, random_state=42),
    "5. AdaBoost": AdaBoostClassifier(n_estimators=100, random_state=42),
    "6. Extra Trees": ExtraTreesClassifier(n_estimators=100, random_state=42, n_jobs=-1),
    "7. K-Nearest Neighbors": KNeighborsClassifier(n_neighbors=5, n_jobs=-1),
    "8. XGBoost": XGBClassifier(n_estimators=100, random_state=42, eval_metric="logloss", n_jobs=-1)
}

# ============================================
# STEP 5: Stratified Cross-Validation
# ============================================

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scoring = ["accuracy", "precision", "recall", "f1", "roc_auc"]

print("=" * 70)
print("STAGE 5: TRAINING & EVALUATING 8 CLASSIFIERS")
print("=" * 70)

results = []

for name, clf in classifiers.items():
    pipeline = Pipeline(
        steps=[
            ("preprocessing", preprocessor),
            ("classifier", clf)
        ]
    )

    cv_results = cross_validate(
        pipeline,
        X_train,
        y_train,
        cv=cv,
        scoring=scoring,
        n_jobs=-1
    )

    results.append({
        "Model": name,
        "Accuracy": cv_results["test_accuracy"].mean(),
        "Precision": cv_results["test_precision"].mean(),
        "Recall": cv_results["test_recall"].mean(),
        "F1-Score": cv_results["test_f1"].mean(),
        "ROC-AUC": cv_results["test_roc_auc"].mean()
    })

# ============================================
# STEP 6: Summary Results Table
# ============================================

results_df = pd.DataFrame(results).sort_values(by="F1-Score", ascending=False)

print("\n" + "=" * 70)
print("STAGE 5: 8-CLASSIFIER COMPARISON TABLE (CROSS-VALIDATION)")
print("=" * 70)

print(
    results_df.to_string(
        index=False,
        float_format=lambda x: f"{x:.4f}"
    )
)
