import pytest
from pydantic import ValidationError

from app.schemas import SimulacaoRequest
from app.services.parcelamento import calcular_parcelamento, simular_parcelamento


@pytest.mark.parametrize(
    ("quantidade_parcelas", "juros_percentual", "valor_juros", "valor_total", "valor_parcela"),
    [
        (1, 0.0, 0.0, 1000.0, 1000.0),
        (3, 10.0, 100.0, 1100.0, 366.67),
        (6, 15.0, 150.0, 1150.0, 191.67),
        (9, 20.0, 200.0, 1200.0, 133.33),
        (12, 25.0, 250.0, 1250.0, 104.17),
    ],
)
def test_calcular_parcelamento_para_parcelas_permitidas(
    quantidade_parcelas: int,
    juros_percentual: float,
    valor_juros: float,
    valor_total: float,
    valor_parcela: float,
) -> None:
    resultado = calcular_parcelamento(valor_divida=1000.0, quantidade_parcelas=quantidade_parcelas)

    assert resultado == {
        "valor_original": 1000.0,
        "juros_percentual": juros_percentual,
        "valor_juros": valor_juros,
        "valor_total": valor_total,
        "parcelas": quantidade_parcelas,
        "valor_parcela": valor_parcela,
    }


@pytest.mark.parametrize("quantidade_parcelas", [1, 3, 6, 9, 12])
def test_simular_parcelamento_retorna_resposta_para_parcelas_permitidas(quantidade_parcelas: int) -> None:
    requisicao = SimulacaoRequest(valor_divida=1000.0, parcelas=quantidade_parcelas)

    resposta = simular_parcelamento(requisicao)

    assert resposta.valor_original == 1000.0
    assert resposta.parcelas == quantidade_parcelas


def test_simulacao_request_rejeita_valor_divida_invalido() -> None:
    with pytest.raises(ValidationError) as exc_info:
        SimulacaoRequest(valor_divida=0, parcelas=3)

    assert "valor_divida deve ser maior que zero" in str(exc_info.value)


def test_simulacao_request_rejeita_parcela_invalida() -> None:
    with pytest.raises(ValidationError) as exc_info:
        SimulacaoRequest(valor_divida=1000.0, parcelas=2)

    assert "parcelas deve ser uma das opcoes: 1, 3, 6, 9 ou 12" in str(exc_info.value)


def test_calcular_parcelamento_rejeita_valor_divida_invalido() -> None:
    with pytest.raises(ValueError) as exc_info:
        calcular_parcelamento(valor_divida=0, quantidade_parcelas=3)

    assert str(exc_info.value) == "valor_divida deve ser maior que zero"


def test_calcular_parcelamento_rejeita_parcela_invalida() -> None:
    with pytest.raises(ValueError) as exc_info:
        calcular_parcelamento(valor_divida=1000.0, quantidade_parcelas=2)

    assert str(exc_info.value) == "parcelas deve ser uma das opcoes: 1, 3, 6, 9 ou 12"
