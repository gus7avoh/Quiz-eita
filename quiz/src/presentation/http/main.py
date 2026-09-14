from fastapi import FastAPI
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s - %(message)s")

from presentation.http.routes.quiz import router as quiz_router

app = FastAPI(
    title="Quiz API",
)

app.include_router(quiz_router)


@app.get("/health")
def health():
    return {"status": "ok"}
