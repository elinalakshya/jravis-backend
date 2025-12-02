import os

# ---------------------------------------------------
# API KEYS
# ---------------------------------------------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
PRINTIFY_API_KEY = os.getenv("PRINTIFY_API_KEY", "")
PAYHIP_API_KEY = os.getenv("PAYHIP_API_KEY", "")
GUMROAD_ACCESS_TOKEN = os.getenv("GUMROAD_ACCESS_TOKEN", "")
MESHY_API_KEY = os.getenv("MESHY_API_KEY", "")

# ---------------------------------------------------
# UNIVERSAL OUTPUT FOLDER (Used by all publishers)
# ---------------------------------------------------
OUTPUT_FOLDER = "generated_output"

# Ensure folder exists
if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# A safe fallback path used when nothing is returned
SAFE_OUTPUT = os.path.join(OUTPUT_FOLDER, "default.txt")
with open(SAFE_OUTPUT, "w") as f:
    f.write("JRAVIS default output placeholder.")

# ---------------------------------------------------
# EMAIL SETTINGS
# ---------------------------------------------------
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_USER = "elinalakshya@gmail.com"
EMAIL_PASS = "znkuyendmrrvhxwp"

# ---------------------------------------------------
# BACKEND URL
# ---------------------------------------------------
BACKEND_URL = "https://jravis-backend.onrender.com"
