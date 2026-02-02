import os, requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("GUMROAD_TOKEN")

def run_gumroad(count=10):
    for i in range(count):
        requests.post(
            "https://api.gumroad.com/v2/products",
            data={
                "access_token": TOKEN,
                "name": f"Productivity Planner #{i+1}",
                "price": 499,
                "published": False
            }
        )
