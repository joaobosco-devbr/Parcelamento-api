from fastapi import APIRouter

from app.schemas import SimulacaoRequest, SimulacaoResponse
from app.services.parcelamento import simular_parcelamento


router = APIRouter(tags=["Simulacao"])


@router.post(
    "/simular",
    response_model=SimulacaoResponse,
    summary="Simula o parcelamento de uma divida",
)
def simular(payload: SimulacaoRequest) -> SimulacaoResponse:
    return simular_parcelamento(payload)
