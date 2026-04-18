from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.rules import PARCELAS_PERMITIDAS


class SimulacaoRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "valor_divida": 1000.0,
                "parcelas": 6,
            }
        }
    )

    valor_divida: float = Field(..., description="Valor original da divida")
    parcelas: int = Field(..., description="Quantidade de parcelas")

    @field_validator("valor_divida")
    @classmethod
    def validar_valor_divida(cls, value: float) -> float:
        if value <= 0:
            raise ValueError("valor_divida deve ser maior que zero")
        return value

    @field_validator("parcelas")
    @classmethod
    def validar_parcelas(cls, value: int) -> int:
        if value not in PARCELAS_PERMITIDAS:
            raise ValueError("parcelas deve ser uma das opcoes: 1, 3, 6, 9 ou 12")
        return value


class SimulacaoResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "valor_original": 1000.0,
                "juros_percentual": 15.0,
                "valor_juros": 150.0,
                "valor_total": 1150.0,
                "parcelas": 6,
                "valor_parcela": 191.67,
            }
        }
    )

    valor_original: float
    juros_percentual: float
    valor_juros: float
    valor_total: float
    parcelas: int
    valor_parcela: float
