from fastapi import APIRouter


router = APIRouter(tags=["Health"])


@router.get("/health", summary="Verifica a saude da aplicacao")
def health() -> dict[str, str]:
    return {"status": "ok"}
