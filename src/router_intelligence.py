from fastapi import APIRouter
from src.intelligence.revenue_predictor import RevenuePredictor
from src.intelligence.system_health import SystemHealth
from src.intelligence.growth_engine import GrowthEngine
from src.intelligence.recommendations import Recommendations
from src.intelligence.weekly_summary import WeeklySummary

router = APIRouter()

@router.get("/intelligence/revenue")
def revenue():
    return RevenuePredictor().predict()

@router.get("/intelligence/health")
def health():
    return SystemHealth().check()

@router.get("/intelligence/predictions")
def predictions():
    return GrowthEngine().score()

@router.get("/intelligence/recommend")
def recommend():
    growth = GrowthEngine().score()
    return Recommendations().generate(growth)

@router.get("/intelligence/weekly")
def weekly():
    rev = RevenuePredictor().predict()
    return WeeklySummary().generate(rev["history"])
