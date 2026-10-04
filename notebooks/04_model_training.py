# ============================================
# Customer Churn Prediction
# Stage 4: Model Training
# ============================================

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# ============================================
# STEP 1: Load Dataset
# ============================================

DATA_PATH = "data/raw/Telco-Customer-Churn.csv"

df = pd.read_csv(DATA_PATH)

print("=" * 70)
print("STAGE 4: MODEL TRAINING")
print("=" * 70)

print("\nOriginal dataset:")
print(df.shape)


# ============================================
# STEP 2: Basic Cleaning
# ============================================

# Remove customer ID
df = df.drop(columns=["customerID"])

# Convert TotalCharges to numeric
df["TotalCharges"] = pd.to_numeric(
    df["TotalCharges"],
    errors="coerce"
)

# Remove rows with missing TotalCharges
df = df.dropna(subset=["TotalCharges"])

# Convert target to 0/1
df["Churn"] = df["Churn"].map({
    "No": 0,
    "Yes": 1
})


# ============================================
# STEP 3: Separate Features and Target
# ============================================

X = df.drop(columns=["Churn"])
y = df["Churn"]

print("\nFeatures shape:", X.shape)
print("Target shape:", y.shape)


# ============================================
# STEP 4: Identify Feature Types
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
# STEP 5: Train-Test Split
# ============================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining data:", X_train.shape)
print("Testing data:", X_test.shape)


# ============================================
# STEP 6: Preprocessing
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
# STEP 7: Create ML Pipeline
# ============================================

model = Pipeline(
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

print("\nPipeline created successfully!")


# ============================================
# STEP 8: Train Model
# ============================================

print("\nTraining Logistic Regression...")

model.fit(X_train, y_train)

print("[OK] Model training completed!")


# ============================================
# STEP 9: Make Predictions
# ============================================

y_pred = model.predict(X_test)


# ============================================
# STEP 10: Evaluate
# ============================================

accuracy = accuracy_score(y_test, y_pred)

print("\n" + "=" * 70)
print("MODEL RESULTS")
print("=" * 70)

print(f"\nAccuracy: {accuracy:.4f}")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

from sklearn.metrics import confusion_matrix
y_pred = model.predict(X_test)

# ============================================
# STEP 10: Confusion Matrix
# ============================================

cm = confusion_matrix(y_test, y_pred)

print("\nConfusion Matrix:")
print(cm)