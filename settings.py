import os

# ---- API KEYS ----
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
PRINTIFY_API_KEY = os.getenv("PRINTIFY_API_KEY", "")
PAYHIP_API_KEY = os.getenv("PAYHIP_API_KEY", "")
MESHY_API_KEY = os.getenv("MESHY_API_KEY", "")
GUMROAD_TOKEN = os.getenv("GUMROAD_TOKEN", "")

# ---- WARNINGS ----
if not GUMROAD_TOKEN:
    print("⚠️ WARNING: GUMROAD_TOKEN not set")

if not OPENAI_API_KEY:
    print("⚠️ WARNING: OPENAI_API_KEY not set")
