import pytest
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)
API_V1_PREFIX = "/api/v1"


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
def test_post_simular_retorna_sucesso_para_parcelas_permitidas(
    quantidade_parcelas: int,
    juros_percentual: float,
    valor_juros: float,
    valor_total: float,
    valor_parcela: float,
) -> None:
    response = client.post(
        f"{API_V1_PREFIX}/simular",
        json={"valor_divida": 1000.0, "parcelas": quantidade_parcelas},
    )

    assert response.status_code == 200
    assert response.json() == {
        "versao_configuracao": 1,
        "valor_original": 1000.0,
        "juros_percentual": juros_percentual,
        "valor_juros": valor_juros,
        "valor_total": valor_total,
        "parcelas": quantidade_parcelas,
        "valor_parcela": valor_parcela,
    }


def test_get_health_retorna_status_e_versao_configuracao() -> None:
    response = client.get(f"{API_V1_PREFIX}/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "produto": "parcelamento",
        "versao_configuracao": 1,
    }


def test_post_simular_retorna_erro_para_valor_divida_invalido() -> None:
    response = client.post(
        f"{API_V1_PREFIX}/simular",
        json={"valor_divida": 0, "parcelas": 3},
    )

    assert response.status_code == 422
    assert response.json() == {
        "code": "validation_error",
        "message": "Dados de entrada invalidos",
        "details": [
            {
                "field": "valor_divida",
                "message": "Value error, valor_divida deve ser maior que zero",
            }
        ],
    }


def test_post_simular_retorna_erro_para_parcela_invalida() -> None:
    response = client.post(
        f"{API_V1_PREFIX}/simular",
        json={"valor_divida": 1000.0, "parcelas": 25},
    )

    assert response.status_code == 422
    assert response.json() == {
        "code": "validation_error",
        "message": "Dados de entrada invalidos",
        "details": [
            {
                "field": "parcelas",
                "message": "Value error, parcelas deve estar entre 1 e 24",
            }
        ],
    }
