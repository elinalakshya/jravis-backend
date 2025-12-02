import requests
import json

def generate_meshy_assets(MESHY_API_KEY):
    print("🎨 Generating Meshy 3D assets...")

    url = "https://api.meshy.ai/v1/text-to-3d"

    headers = {
        "Authorization": f"Bearer {MESHY_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": "3d object, low poly, clean style, marketplace ready",
        "output_format": "glb"
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()

        print("📦 Meshy Response:", json.dumps(data, indent=2))

        # In future: save GLB file + send to worker output folder
        return data

    except Exception as e:
        print("❌ Meshy generation error:", e)
        return None
