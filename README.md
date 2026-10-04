# Customer Churn Prediction - End-to-End Machine Learning System

[![Python 3.14](https://img.shields.io/badge/Python-3.14-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.142-009688?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-17-61DAFB?style=flat&logo=react&logoColor=black)](https://reactjs.org/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-1.3+-F7931E?style=flat&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)
[![CI/CD](https://img.shields.io/badge/GitHub_Actions-Automated-2088FF?style=flat&logo=github-actions&logoColor=white)](https://github.com/features/actions)

An end-to-end, production-grade Machine Learning system designed to predict telecom customer churn. Structured across **10 progressive ML stages**, from exploratory analysis to hyperparameter tuning, unsupervised clustering, FastAPI backend, React web portal, Docker containerization, and GitHub Actions CI/CD.

---

## 🗺️ 10 Progressive Stages Curriculum

| Stage | Name & Core Concepts | Implementation Artifact / Script | Status |
| :---: | :--- | :--- | :---: |
| **1** | **Project Setup & Data Inspection** (shape, types, nulls, duplicates) | [notebooks/01_data_inspection.py](file:///C:/Users/Bhoomika%20s%20a/OneDrive/Desktop/Customer-Churn-Prediction/notebooks/01_data_inspection.py) | ✅ Completed |
| **2** | **EDA** (visualizations, distributions, correlations, outliers) | [notebooks/02_eda.py](file:///C:/Users/Bhoomika%20s%20a/OneDrive/Desktop/Customer-Churn-Prediction/notebooks/02_eda.py) | ✅ Completed |
| **3** | **Data Cleaning** (missing values, duplicates, type fixes) | [notebooks/03_preprocessing.py](file:///C:/Users/Bhoomika%20s%20a/OneDrive/Desktop/Customer-Churn-Prediction/notebooks/03_preprocessing.py) | ✅ Completed |
| **4** | **Feature Engineering** (encoding, scaling, train/val/test split, data leakage prevention) | [notebooks/04_model_training.py](file:///C:/Users/Bhoomika%20s%20a/OneDrive/Desktop/Customer-Churn-Prediction/notebooks/04_model_training.py) | ✅ Completed |
| **5** | **Training 8 Classifiers** (Logistic Regression $\rightarrow$ XGBoost) | [notebooks/05_train_8_classifiers.py](file:///C:/Users/Bhoomika%20s%20a/OneDrive/Desktop/Customer-Churn-Prediction/notebooks/05_train_8_classifiers.py) | ✅ Completed |
| **6** | **Evaluation & Tuning** (confusion matrix, recall, F1, ROC-AUC, CV, hyperparameter tuning) | [notebooks/08_hyperparameter_tuning.py](file:///C:/Users/Bhoomika%20s%20a/OneDrive/Desktop/Customer-Churn-Prediction/notebooks/08_hyperparameter_tuning.py) | ✅ Completed |
| **7** | **Unsupervised Learning** (K-Means clustering, elbow method, customer segmentation) | [notebooks/07_kmeans_clustering.py](file:///C:/Users/Bhoomika%20s%20a/OneDrive/Desktop/Customer-Churn-Prediction/notebooks/07_kmeans_clustering.py) | ✅ Completed |
| **8** | **Final Model Selection & Saving** (joblib serialization & metadata) | [notebooks/10_save_final_model.py](file:///C:/Users/Bhoomika%20s%20a/OneDrive/Desktop/Customer-Churn-Prediction/notebooks/10_save_final_model.py) | ✅ Completed |
| **9** | **FastAPI Backend + React Frontend** (REST API & Web Portal UI) | [backend/main.py](file:///C:/Users/Bhoomika%20s%20a/OneDrive/Desktop/Customer-Churn-Prediction/backend/main.py) & [frontend/App.jsx](file:///C:/Users/Bhoomika%20s%20a/OneDrive/Desktop/Customer-Churn-Prediction/frontend/App.jsx) | ✅ Completed |
| **10** | **Docker & GitHub Actions CI/CD** (containerization, automated test pipeline) | [Dockerfile](file:///C:/Users/Bhoomika%20s%20a/OneDrive/Desktop/Customer-Churn-Prediction/Dockerfile) & [.github/workflows/ci-cd.yml](file:///C:/Users/Bhoomika%20s%20a/OneDrive/Desktop/Customer-Churn-Prediction/.github/workflows/ci-cd.yml) | ✅ Completed |

---

## 📊 Stage 5: 8-Classifier Comparison Table

| Model Classifier | Accuracy | Precision | Recall | F1-Score | ROC-AUC |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **1. Logistic Regression** | 80.34% | 65.68% | 54.65% | **0.5964** | 0.8461 |
| **5. AdaBoost** | 80.44% | 67.05% | 52.11% | 0.5860 | 0.8489 |
| **4. Gradient Boosting** | 80.05% | 66.19% | 51.10% | 0.5763 | 0.8477 |
| **8. XGBoost** | 78.92% | 62.37% | 51.97% | 0.5665 | 0.8279 |
| **3. Random Forest** | 79.50% | 65.20% | 49.10% | 0.5598 | 0.8268 |
| **2. Decision Tree** | 79.09% | 64.11% | 49.50% | 0.5513 | 0.8294 |
| **7. K-Nearest Neighbors** | 76.27% | 55.63% | 52.84% | 0.5420 | 0.7811 |
| **6. Extra Trees** | 77.99% | 60.88% | 48.23% | 0.5379 | 0.8043 |

*After Stage 6 Hyperparameter Tuning with class balancing (`class_weight='balanced'`), **Random Forest** achieved an optimal **81.28% Recall** and **0.8383 ROC-AUC** on the holdout test set.*

---

## ⚡ Quickstart Commands

```powershell
# 1. Run 8 Classifiers Comparison (Stage 5)
python notebooks/05_train_8_classifiers.py

# 2. Run Unsupervised K-Means Clustering (Stage 7)
python notebooks/07_kmeans_clustering.py

# 3. Save Final Model Artifacts (Stage 8)
python notebooks/10_save_final_model.py

# 4. Run Automated Pytest Suite
python -m pytest tests/

# 5. Launch FastAPI Backend Server (Stage 9)
python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000

# 6. Build Docker Container (Stage 10)
docker build -t customer-churn-api:latest .
```
