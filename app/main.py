import os
import time
from collections import defaultdict
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api.routes.health import router as health_router
from app.api.routes.search import router as search_router
from app.api.routes.recommend import router as recommend_router

app = FastAPI(
    title="Book Recommendation Platform",
    description="Hybrid, explainable book recommendation system",
    version="1.0.0"
)

RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS", "60"))
RATE_LIMIT_WINDOW_SEC = int(os.getenv("RATE_LIMIT_WINDOW_SEC", "60"))

_rate_window = defaultdict(list)


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    now = time.time()
    client_ip = request.client.host if request.client else "unknown"
    window_start = now - RATE_LIMIT_WINDOW_SEC

    bucket = _rate_window[client_ip]
    bucket[:] = [t for t in bucket if t > window_start]

    if len(bucket) >= RATE_LIMIT_REQUESTS:
        return JSONResponse(
            status_code=429,
            content={"detail": "Too many requests. Please try again later."}
        )

    bucket.append(now)
    return await call_next(request)


app.include_router(health_router)
app.include_router(search_router)
app.include_router(recommend_router)
