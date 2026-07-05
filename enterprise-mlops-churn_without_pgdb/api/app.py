"""
app.py
------
FastAPI application exposing `/`, `/health`, `/predict`, and `/metrics`
endpoints for the Customer Churn Prediction Platform.

Run locally with:
    uvicorn api.app:app --reload --port 8000
"""

from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.config import settings
from src.logger import get_logger
from src.utils import load_json

logger = get_logger(__name__)

_predictor = None  # lazily loaded on startup


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _predictor
    try:
        from src.predict import ChurnPredictor
        _predictor = ChurnPredictor()
        logger.info("Model artifacts loaded successfully")
    except FileNotFoundError:
        logger.warning(
            "Model artifacts not found. Run `python -m src.train` before serving predictions."
        )
        _predictor = None
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)


class CustomerRecord(BaseModel):
    gender: str = Field(..., examples=["Female"])
    SeniorCitizen: int = Field(..., examples=[0])
    Partner: str = Field(..., examples=["Yes"])
    Dependents: str = Field(..., examples=["No"])
    tenure: int = Field(..., ge=0, examples=[5])
    InternetService: str = Field(..., examples=["Fiber optic"])
    Contract: str = Field(..., examples=["Month-to-month"])
    PaperlessBilling: str = Field(..., examples=["Yes"])
    PaymentMethod: str = Field(..., examples=["Electronic check"])
    MonthlyCharges: float = Field(..., ge=0, examples=[85.5])
    TotalCharges: float = Field(..., ge=0, examples=[427.5])


class PredictionResponse(BaseModel):
    churn_prediction: str
    churn_probability: float


@app.get("/")
def root():
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
    }


@app.get("/health")
def health():
    model_ready = _predictor is not None
    return {
        "status": "healthy" if model_ready else "degraded",
        "model_loaded": model_ready,
    }


@app.post("/predict", response_model=PredictionResponse)
def predict(record: CustomerRecord):
    if _predictor is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Train the model first with `python -m src.train`.",
        )
    try:
        result = _predictor.predict(record.model_dump())
        return result
    except Exception as exc:
        logger.exception("Prediction failed")
        raise HTTPException(status_code=400, detail=str(exc))


@app.get("/metrics")
def metrics():
    try:
        return load_json(settings.METRICS_FILE)
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="No metrics found. Train the model first with `python -m src.train`.",
        )
