# src/router_streams.py
from fastapi import APIRouter, Depends
from utils.security import verify_api_key
from utils.file_reader import get_latest_file

router = APIRouter()

STREAMS = [
    "gumroad",
    "payhip",
    "blog",
    "newsletter",
    "affiliate_funnel",
    "shopify",
    "template_machine"
]

@router.get("/streams")
def list_streams(auth=Depends(verify_api_key)):
    return {"streams": STREAMS}

@router.get("/streams/{stream_name}/latest")
def get_latest(stream_name: str, auth=Depends(verify_api_key)):
    if stream_name not in STREAMS:
        return {"error": "Invalid stream name"}

    data = get_latest_file(stream_name)
    if not data:
        return {"error": "No output found for this stream"}

    return {"stream": stream_name, "latest_output": data}
