from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import sys

# Add src to path so imports work correctly
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.lift_calculator import get_lift_results
from src.settlement_engine import get_settlement_results
from src.reliability_scorer import get_reliability_scores
from src.ai_insights import get_insights
import math
import numpy as np

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For local development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def clean_data(df):
    """Replace NaN, Inf, -Inf with None for JSON serialization."""
    df = df.replace([np.inf, -np.inf], "Infinity")
    df = df.fillna("N/A")
    return df.to_dict(orient="records")

@app.get("/api/campaigns")
def get_campaigns():
    df = get_lift_results("data")
    return clean_data(df)

@app.get("/api/settlement")
def get_settlement():
    df = get_settlement_results("data")
    return clean_data(df)

@app.get("/api/reliability")
def get_reliability():
    df = get_reliability_scores("data")
    return clean_data(df)

@app.get("/api/insights/{campaign_id}")
def get_campaign_insights(campaign_id: str):
    settlement_df = get_settlement_results("data")
    lift_df = get_lift_results("data")
    reliability_df = get_reliability_scores("data")
    
    result = get_insights(campaign_id, settlement_df, lift_df, reliability_df, use_ai=True)
    return result.to_dict()
