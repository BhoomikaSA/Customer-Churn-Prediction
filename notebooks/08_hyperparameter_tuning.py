# ============================================
# Customer Churn Prediction
# Stage 8: Hyperparameter Tuning
# ============================================

import pandas as pd

from sklearn.model_selection import (
    StratifiedKFold,
    RandomizedSearchCV,
    train_test_split
)

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import (
    OneHotEncoder,
    StandardScaler
)

from sklearn.pipeline import Pipeline

from sklearn.linear_model import LogisticRegression

from sklearn.ensemble import RandomForestClassifier

from xgboost import XGBClassifier


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

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    stratify=y,
    random_state=42
)


numerical_features = X.select_dtypes(
    include=["int64", "float64"]
).columns.tolist()

categorical_features = X.select_dtypes(
    include=["str"]
).columns.tolist()


# ============================================
# STEP 3: Preprocessing
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
# STEP 4: Cross-Validation
# ============================================

cv = StratifiedKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)


# ============================================
# STEP 5: Logistic Regression
# ============================================

print("=" * 70)
print("LOGISTIC REGRESSION TUNING")
print("=" * 70)

logistic_pipeline = Pipeline(
    steps=[
        ("preprocessing", preprocessor),

        (
            "classifier",
            LogisticRegression(
                max_iter=1000,
                random_state=42
            )
        )
    ]
)


logistic_params = {
    "classifier__C": [
        0.01,
        0.1,
        1,
        10,
        100
    ],

    "classifier__class_weight": [
        None,
        "balanced"
    ]
}


logistic_search = RandomizedSearchCV(
    logistic_pipeline,
    logistic_params,
    n_iter=10,
    scoring="f1",
    cv=cv,
    random_state=42,
    n_jobs=-1
)


logistic_search.fit(X_train, y_train)


print("\nBest parameters:")
print(logistic_search.best_params_)

print("\nBest F1 score:")
print(f"{logistic_search.best_score_:.4f}")


# ============================================
# STEP 6: Random Forest
# ============================================

print("\n" + "=" * 70)
print("RANDOM FOREST TUNING")
print("=" * 70)


rf_pipeline = Pipeline(
    steps=[
        ("preprocessing", preprocessor),

        (
            "classifier",
            RandomForestClassifier(
                random_state=42,
                n_jobs=-1
            )
        )
    ]
)


rf_params = {
    "classifier__n_estimators": [
        100,
        200,
        300
    ],

    "classifier__max_depth": [
        5,
        8,
        12,
        None
    ],

    "classifier__min_samples_split": [
        2,
        5,
        10
    ],

    "classifier__min_samples_leaf": [
        1,
        2,
        4
    ],

    "classifier__class_weight": [
        None,
        "balanced"
    ]
}


rf_search = RandomizedSearchCV(
    rf_pipeline,
    rf_params,
    n_iter=15,
    scoring="f1",
    cv=cv,
    random_state=42,
    n_jobs=-1
)


rf_search.fit(X_train, y_train)


print("\nBest parameters:")
print(rf_search.best_params_)

print("\nBest F1 score:")
print(f"{rf_search.best_score_:.4f}")


# ============================================
# STEP 7: XGBoost
# ============================================

print("\n" + "=" * 70)
print("XGBOOST TUNING")
print("=" * 70)


xgb_pipeline = Pipeline(
    steps=[
        ("preprocessing", preprocessor),

        (
            "classifier",
            XGBClassifier(
                random_state=42,
                eval_metric="logloss",
                n_jobs=-1
            )
        )
    ]
)


xgb_params = {
    "classifier__n_estimators": [
        100,
        200,
        300
    ],

    "classifier__max_depth": [
        3,
        4,
        5,
        6
    ],

    "classifier__learning_rate": [
        0.01,
        0.05,
        0.1,
        0.2
    ],

    "classifier__subsample": [
        0.7,
        0.8,
        1.0
    ],

    "classifier__colsample_bytree": [
        0.7,
        0.8,
        1.0
    ]
}


xgb_search = RandomizedSearchCV(
    xgb_pipeline,
    xgb_params,
    n_iter=20,
    scoring="f1",
    cv=cv,
    random_state=42,
    n_jobs=-1
)


xgb_search.fit(X_train, y_train)


print("\nBest parameters:")
print(xgb_search.best_params_)

print("\nBest F1 score:")
print(f"{xgb_search.best_score_:.4f}")


# ============================================
# STEP 8: Final Comparison
# ============================================

print("\n" + "=" * 70)
print("HYPERPARAMETER TUNING RESULTS")
print("=" * 70)

results = pd.DataFrame({
    "Model": [
        "Logistic Regression",
        "Random Forest",
        "XGBoost"
    ],

    "Best F1": [
        logistic_search.best_score_,
        rf_search.best_score_,
        xgb_search.best_score_
    ]
})

print(
    results.to_string(
        index=False,
        float_format=lambda x: f"{x:.4f}"
    )
)