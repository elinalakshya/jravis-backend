# src/router_intelligence.py

from fastapi import APIRouter
from src.intelligence.revenue_tracker import (
    get_today_revenue, get_week_revenue, log_revenue
)
from src.intelligence.optimizer import run_optimizer
from src.intelligence.market_pulse import get_market_pulse
from src.intelligence.insights import generate_insights, generate_weekly_summary

router = APIRouter(prefix="/intelligence", tags=["intelligence"])


@router.get("/revenue/today")
def today_revenue():
    return get_today_revenue()


@router.get("/revenue/week")
def week_revenue():
    return get_week_revenue()


@router.post("/revenue/log")
def revenue_log(stream: str, amount: float):
    return log_revenue(stream, amount)


@router.get("/optimizer/run")
def optimizer_run():
    return run_optimizer()


@router.get("/market")
def market_trends():
    return {"trends": get_market_pulse()}


@router.get("/insights")
def insights_today():
    return generate_insights()


@router.get("/insights/weekly")
def insights_weekly():
    return generate_weekly_summary()
