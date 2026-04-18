from decimal import Decimal, ROUND_HALF_UP

from app.rules import JUROS_POR_PARCELAS, PARCELAS_PERMITIDAS
from app.schemas import SimulacaoRequest, SimulacaoResponse


TWO_DECIMAL_PLACES = Decimal("0.01")


def arredondar_moeda(valor: Decimal) -> float:
    return float(valor.quantize(TWO_DECIMAL_PLACES, rounding=ROUND_HALF_UP))


def calcular_parcelamento(valor_divida: float, quantidade_parcelas: int) -> dict[str, float | int]:
    if valor_divida <= 0:
        raise ValueError("valor_divida deve ser maior que zero")

    if quantidade_parcelas not in PARCELAS_PERMITIDAS:
        raise ValueError("parcelas deve ser uma das opcoes: 1, 3, 6, 9 ou 12")

    percentual_juros = Decimal(str(JUROS_POR_PARCELAS[quantidade_parcelas]))
    valor_original = Decimal(str(valor_divida))
    valor_juros = valor_original * (percentual_juros / Decimal("100"))
    valor_total = valor_original + valor_juros
    valor_parcela = valor_total / Decimal(str(quantidade_parcelas))

    return {
        "valor_original": arredondar_moeda(valor_original),
        "juros_percentual": arredondar_moeda(percentual_juros),
        "valor_juros": arredondar_moeda(valor_juros),
        "valor_total": arredondar_moeda(valor_total),
        "parcelas": quantidade_parcelas,
        "valor_parcela": arredondar_moeda(valor_parcela),
    }


def simular_parcelamento(payload: SimulacaoRequest) -> SimulacaoResponse:
    resultado_parcelamento = calcular_parcelamento(
        valor_divida=payload.valor_divida,
        quantidade_parcelas=payload.parcelas,
    )
    return SimulacaoResponse(**resultado_parcelamento)
