import pytest
from pydantic import ValidationError

from app.settings import get_parcelamento_config
from app.schemas import SimulacaoRequest
from app.services.parcelamento import calcular_parcelamento, simular_parcelamento


@pytest.mark.parametrize(
    ("quantidade_parcelas", "juros_percentual", "valor_juros", "valor_total", "valor_parcela"),
    [
        (1, 0.0, 0.0, 1000.0, 1000.0),
        (2, 10.0, 100.0, 1100.0, 550.0),
        (3, 10.0, 100.0, 1100.0, 366.67),
        (4, 15.0, 150.0, 1150.0, 287.5),
        (6, 15.0, 150.0, 1150.0, 191.67),
        (8, 20.0, 200.0, 1200.0, 150.0),
        (9, 20.0, 200.0, 1200.0, 133.33),
        (10, 25.0, 250.0, 1250.0, 125.0),
        (12, 25.0, 250.0, 1250.0, 104.17),
        (15, 30.0, 300.0, 1300.0, 86.67),
        (18, 35.0, 350.0, 1350.0, 75.0),
        (21, 40.0, 400.0, 1400.0, 66.67),
        (24, 45.0, 450.0, 1450.0, 60.42),
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
        "versao_configuracao": 1,
        "valor_original": 1000.0,
        "juros_percentual": juros_percentual,
        "valor_juros": valor_juros,
        "valor_total": valor_total,
        "parcelas": quantidade_parcelas,
        "valor_parcela": valor_parcela,
    }


@pytest.mark.parametrize("quantidade_parcelas", [1, 2, 8, 12, 24])
def test_simular_parcelamento_retorna_resposta_para_parcelas_permitidas(quantidade_parcelas: int) -> None:
    requisicao = SimulacaoRequest(valor_divida=1000.0, parcelas=quantidade_parcelas)

    resposta = simular_parcelamento(requisicao)

    assert resposta.versao_configuracao == 1
    assert resposta.valor_original == 1000.0
    assert resposta.parcelas == quantidade_parcelas


def test_simulacao_request_rejeita_valor_divida_invalido() -> None:
    with pytest.raises(ValidationError) as exc_info:
        SimulacaoRequest(valor_divida=0, parcelas=3)

    assert "valor_divida deve ser maior que zero" in str(exc_info.value)


def test_simulacao_request_rejeita_parcela_invalida() -> None:
    with pytest.raises(ValidationError) as exc_info:
        SimulacaoRequest(valor_divida=1000.0, parcelas=25)

    assert "parcelas deve estar entre 1 e 24" in str(exc_info.value)


def test_calcular_parcelamento_rejeita_valor_divida_invalido() -> None:
    with pytest.raises(ValueError) as exc_info:
        calcular_parcelamento(valor_divida=0, quantidade_parcelas=3)

    assert str(exc_info.value) == "valor_divida deve ser maior que zero"


def test_calcular_parcelamento_rejeita_parcela_invalida() -> None:
    with pytest.raises(ValueError) as exc_info:
        calcular_parcelamento(valor_divida=1000.0, quantidade_parcelas=25)

    assert str(exc_info.value) == "parcelas deve estar entre 1 e 24"


def test_configuracao_versionada_de_parcelamento_e_carregada_com_sucesso() -> None:
    config = get_parcelamento_config()

    assert config.produto == "parcelamento"
    assert config.versao == 1
    assert config.parcelas.minimo == 1
    assert config.parcelas.maximo == 24
    assert config.juros_por_limite[-1].limite_superior == 24
