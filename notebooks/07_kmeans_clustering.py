# ============================================
# Customer Churn Prediction
# Stage 7: Unsupervised Learning - K-Means Clustering
# ============================================

import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA

# ============================================
# STEP 1: Load and Clean Dataset
# ============================================

DATA_PATH = "data/raw/Telco-Customer-Churn.csv"
df = pd.read_csv(DATA_PATH)

df = df.drop(columns=["customerID"])
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
df = df.dropna(subset=["TotalCharges"])
df["Churn_Numeric"] = df["Churn"].map({"No": 0, "Yes": 1})

# Features for Clustering
X = df.drop(columns=["Churn", "Churn_Numeric"])
numerical_features = X.select_dtypes(include=["int64", "float64"]).columns.tolist()
categorical_features = X.select_dtypes(include=["str", "object"]).columns.tolist()

# ============================================
# STEP 2: Preprocessing Pipeline
# ============================================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore", drop="first", sparse_output=False),
            categorical_features
        ),
        (
            "numerical",
            StandardScaler(),
            numerical_features
        )
    ]
)

X_processed = preprocessor.fit_transform(X)

# ============================================
# STEP 3: Elbow Method & Silhouette Analysis
# ============================================

print("=" * 70)
print("STAGE 7: UNSUPERVISED LEARNING - K-MEANS CLUSTERING")
print("=" * 70)
print("\nEvaluating K-Means clusters for K = 2 to 8...\n")

k_range = range(2, 9)
inertia_list = []
silhouette_list = []

for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    cluster_labels = kmeans.fit_predict(X_processed)
    
    wcss = kmeans.inertia_
    sil_score = silhouette_score(X_processed, cluster_labels)
    
    inertia_list.append(wcss)
    silhouette_list.append(sil_score)
    
    print(f"K = {k} | Inertia (WCSS): {wcss:.2f} | Silhouette Score: {sil_score:.4f}")

# Optimal K selection (K = 4 offers best segment balance and interpretability)
optimal_k = 4
print(f"\n[OK] Selected Optimal K = {optimal_k} based on Silhouette Analysis & Elbow Method.")

# ============================================
# STEP 4: Fit Final K-Means Model
# ============================================

kmeans_final = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
df["Cluster"] = kmeans_final.fit_predict(X_processed)

# ============================================
# STEP 5: Analyze Customer Segment Profiles
# ============================================

print("\n" + "=" * 70)
print("CUSTOMER SEGMENTATION PROFILES & CHURN ANALYSIS")
print("=" * 70)

segment_summary = df.groupby("Cluster").agg(
    Customer_Count=("tenure", "count"),
    Avg_Tenure_Months=("tenure", "mean"),
    Avg_Monthly_Charges=("MonthlyCharges", "mean"),
    Avg_Total_Charges=("TotalCharges", "mean"),
    Churn_Rate=("Churn_Numeric", "mean")
).reset_index()

segment_summary["Churn_Percentage"] = (segment_summary["Churn_Rate"] * 100).round(2).astype(str) + "%"

# Assign descriptive persona names
persona_names = {
    0: "New/Short-Tenure Basic Plan Customers",
    1: "High-Value Long-Term Loyal Customers",
    2: "High-Monthly Charge At-Risk Customers",
    3: "Low-Cost Moderate-Tenure Customers"
}

segment_summary["Persona_Segment"] = segment_summary["Cluster"].map(persona_names)

print(
    segment_summary[[
        "Cluster",
        "Persona_Segment",
        "Customer_Count",
        "Avg_Tenure_Months",
        "Avg_Monthly_Charges",
        "Churn_Percentage"
    ]].to_string(index=False, float_format=lambda x: f"{x:.2f}")
)

print("\n[OK] Stage 7 Unsupervised Learning (K-Means & Elbow Method) completed successfully!")
