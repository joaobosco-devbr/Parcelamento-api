from fastapi import APIRouter

from app.schemas import ErrorResponse, SimulacaoRequest, SimulacaoResponse
from app.services.parcelamento import simular_parcelamento


router = APIRouter(tags=["Simulacao"])


@router.post(
    "/simular",
    response_model=SimulacaoResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Erro de regra de negocio"},
        422: {"model": ErrorResponse, "description": "Erro de validacao"},
    },
    summary="Simula o parcelamento de uma divida",
)
def simular(payload: SimulacaoRequest) -> SimulacaoResponse:
    return simular_parcelamento(payload)
