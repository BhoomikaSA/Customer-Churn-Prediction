# ============================================
# Customer Churn Prediction - Backend API
# Stage 11: FastAPI Real-Time REST Service
# ============================================

import os
import json
import joblib
import pandas as pd
from typing import Dict, Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Initialize FastAPI App
app = FastAPI(
    title="Customer Churn Prediction API",
    description="Real-time machine learning REST API for predicting customer churn using Random Forest Classifier.",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Paths to model artifacts
MODEL_PATH = os.path.join("models", "best_model_pipeline.joblib")
METADATA_PATH = os.path.join("models", "model_metadata.json")

# Global variables for model and metadata
model_pipeline = None
model_metadata = None


def load_artifacts():
    global model_pipeline, model_metadata
    if model_pipeline is None and os.path.exists(MODEL_PATH):
        try:
            model_pipeline = joblib.load(MODEL_PATH)
            print(f"[OK] Model pipeline loaded successfully from: {MODEL_PATH}")
        except Exception as e:
            print(f"[ERROR] Failed to load model pipeline: {str(e)}")

    if model_metadata is None and os.path.exists(METADATA_PATH):
        try:
            with open(METADATA_PATH, "r") as f:
                model_metadata = json.load(f)
            print(f"[OK] Metadata loaded successfully from: {METADATA_PATH}")
        except Exception as e:
            print(f"[ERROR] Failed to load metadata: {str(e)}")


# Load artifacts on module import
load_artifacts()


@app.on_event("startup")
def startup_event():
    load_artifacts()


# Pydantic Input Schema with Pydantic v2 json_schema_extra
class CustomerData(BaseModel):
    gender: str = Field(..., json_schema_extra={"example": "Female"})
    SeniorCitizen: int = Field(..., json_schema_extra={"example": 0})
    Partner: str = Field(..., json_schema_extra={"example": "Yes"})
    Dependents: str = Field(..., json_schema_extra={"example": "No"})
    tenure: int = Field(..., json_schema_extra={"example": 1})
    PhoneService: str = Field(..., json_schema_extra={"example": "No"})
    MultipleLines: str = Field(..., json_schema_extra={"example": "No phone service"})
    InternetService: str = Field(..., json_schema_extra={"example": "DSL"})
    OnlineSecurity: str = Field(..., json_schema_extra={"example": "No"})
    OnlineBackup: str = Field(..., json_schema_extra={"example": "Yes"})
    DeviceProtection: str = Field(..., json_schema_extra={"example": "No"})
    TechSupport: str = Field(..., json_schema_extra={"example": "No"})
    StreamingTV: str = Field(..., json_schema_extra={"example": "No"})
    StreamingMovies: str = Field(..., json_schema_extra={"example": "No"})
    Contract: str = Field(..., json_schema_extra={"example": "Month-to-month"})
    PaperlessBilling: str = Field(..., json_schema_extra={"example": "Yes"})
    PaymentMethod: str = Field(..., json_schema_extra={"example": "Electronic check"})
    MonthlyCharges: float = Field(..., json_schema_extra={"example": 29.85})
    TotalCharges: float = Field(..., json_schema_extra={"example": 29.85})


# Response Schema
class PredictionResponse(BaseModel):
    prediction: str
    churn_probability: float
    risk_level: str
    model_name: str


@app.get("/")
def read_root():
    return {
        "message": "Customer Churn Prediction API is running.",
        "status": "healthy",
        "model_loaded": model_pipeline is not None
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "model_pipeline_status": "loaded" if model_pipeline else "not_loaded"
    }


@app.post("/predict", response_model=PredictionResponse)
def predict_churn(customer: CustomerData):
    load_artifacts()
    if model_pipeline is None:
        raise HTTPException(
            status_code=500,
            detail="Model pipeline is not loaded on server."
        )

    try:
        # Convert input Pydantic model to pandas DataFrame
        input_data = pd.DataFrame([customer.model_dump()])

        # Make prediction
        pred_int = model_pipeline.predict(input_data)[0]
        churn_prob = float(model_pipeline.predict_proba(input_data)[0][1])

        churn_label = "Yes" if pred_int == 1 else "No"

        # Determine Risk Category
        if churn_prob >= 0.70:
            risk = "High Risk"
        elif churn_prob >= 0.40:
            risk = "Medium Risk"
        else:
            risk = "Low Risk"

        return PredictionResponse(
            prediction=churn_label,
            churn_probability=round(churn_prob, 4),
            risk_level=risk,
            model_name="RandomForestClassifier (Tuned)"
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Prediction error: {str(e)}"
        )
