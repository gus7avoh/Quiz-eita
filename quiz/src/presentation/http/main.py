from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from redis.exceptions import RedisError
import logging
import os
from pathlib import Path
from fastapi.staticfiles import StaticFiles

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s - %(message)s")

from presentation.http.routes.quiz import router as quiz_router
from presentation.http.routes.ranking import router as ranking_router

app = FastAPI(
    title="Quiz API",
)

app.include_router(quiz_router)
app.include_router(ranking_router)


@app.exception_handler(RedisError)
async def redis_error_handler(request, exc):
    logging.getLogger(__name__).error("Falha na operação Redis", exc_info=exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "Falha ao acessar o Redis. Tente novamente."},
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        origin.strip()
        for origin in os.getenv(
            "CORS_ORIGINS",
            "http://localhost:5173,http://localhost:5174",
        ).split(",")
        if origin.strip()
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


# Keep this mount after every API route so /health, /docs and API routes are
# handled by FastAPI before the catch-all frontend mount.
frontend_dir = Path(__file__).resolve().parents[4] / "frontend"
if frontend_dir.is_dir():
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
