# ============================================
# JRAVIS BACKEND + DAILY FACTORY (PRODUCTION)
# ============================================

from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import pytz
import os

# --------------------------------------------
# Import your factory
# --------------------------------------------
from daily_factory import run_factory

app = FastAPI()


# ============================================
# BASIC HEALTH CHECK
# ============================================
@app.get("/healthz")
def health():
    return {"status": "ok"}


# ============================================
# MANUAL TRIGGER (optional but useful)
# You can hit this URL anytime to run drafts
# ============================================
@app.get("/run-drafts-now")
@app.post("/run-drafts-now")
def manual_run():
    run_factory()
    return {"status": "Draft factory executed manually"}


# ============================================
# SCHEDULER (NO RENDER CRON NEEDED)
# ============================================

IST = pytz.timezone("Asia/Kolkata")
scheduler = BackgroundScheduler(timezone=IST)


def scheduled_job():
    print("🚀 JRAVIS DAILY FACTORY STARTED:", datetime.now())
    run_factory()
    print("✅ JRAVIS DAILY FACTORY COMPLETED")


# Run daily at 9:30 AM IST
scheduler.add_job(
    scheduled_job,
    trigger="cron",
    hour=9,
    minute=30
)

scheduler.start()


# ============================================
# STARTUP LOG
# ============================================
@app.on_event("startup")
def startup_event():
    print("✅ JRAVIS Backend running with internal scheduler")
