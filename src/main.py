from fastapi import Request
from fastapi.responses import JSONResponse

BLOCKED_IP = "74.220.48.249"

@app.middleware("http")
async def block_old_caller(request: Request, call_next):
    client_ip = request.client.host
    if client_ip == BLOCKED_IP:
        return JSONResponse({"error": "Forbidden"}, status_code=403)
    return await call_next(request)
