from fastapi import FastAPI

from app.routers.health import router as health_router
from app.routers.simulacao import router as simulacao_router


app = FastAPI(
    title="API de Simulacao de Parcelamento",
    description=(
        "API REST para simulacao de parcelamento com regras fixas de juros "
        "por quantidade de parcelas."
    ),
    version="1.0.0",
)
app.include_router(health_router)
app.include_router(simulacao_router)
