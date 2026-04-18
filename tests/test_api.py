import pytest
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


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
def test_post_simular_retorna_sucesso_para_parcelas_permitidas(
    quantidade_parcelas: int,
    juros_percentual: float,
    valor_juros: float,
    valor_total: float,
    valor_parcela: float,
) -> None:
    response = client.post(
        "/simular",
        json={"valor_divida": 1000.0, "parcelas": quantidade_parcelas},
    )

    assert response.status_code == 200
    assert response.json() == {
        "valor_original": 1000.0,
        "juros_percentual": juros_percentual,
        "valor_juros": valor_juros,
        "valor_total": valor_total,
        "parcelas": quantidade_parcelas,
        "valor_parcela": valor_parcela,
    }


def test_post_simular_retorna_erro_para_valor_divida_invalido() -> None:
    response = client.post(
        "/simular",
        json={"valor_divida": 0, "parcelas": 3},
    )

    assert response.status_code == 422


def test_post_simular_retorna_erro_para_parcela_invalida() -> None:
    response = client.post(
        "/simular",
        json={"valor_divida": 1000.0, "parcelas": 2},
    )

    assert response.status_code == 422
