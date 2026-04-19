from fastapi import APIRouter

from app.settings import get_parcelamento_config


router = APIRouter(tags=["Health"])


@router.get("/health", summary="Verifica a saude da aplicacao")
def health() -> dict[str, str | int]:
    config = get_parcelamento_config()
    return {
        "status": "ok",
        "produto": config.produto,
        "versao_configuracao": config.versao,
    }
