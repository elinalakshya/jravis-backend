import requests
import uuid
from settings import MESHY_API_KEY, OPENAI_API_KEY
import openai

openai.api_key = OPENAI_API_KEY

def publish_meshy_asset():
    prompt = f"3D model of {uuid.uuid4().hex[:6]} object, clean, detailed, white background"

    print("🧱 Generating Meshy Asset:", prompt)

    url = "https://api.meshy.ai/v1/text-to-3d"
    headers = {"Authorization": f"Bearer {MESHY_API_KEY}"}

    data = {"prompt": prompt}

    resp = requests.post(url, json=data, headers=headers).json()
    print("🔧 Meshy Response:", resp)
    return resp
  
