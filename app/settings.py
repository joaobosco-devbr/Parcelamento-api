from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from pydantic import BaseModel, Field, model_validator


class ParcelaRangeConfig(BaseModel):
    minimo: int = Field(..., ge=1)
    maximo: int = Field(..., ge=1)

    @model_validator(mode="after")
    def validar_intervalo(self) -> "ParcelaRangeConfig":
        if self.minimo > self.maximo:
            raise ValueError("intervalo de parcelas invalido")
        return self


class JurosPorLimiteConfig(BaseModel):
    limite_superior: int = Field(..., ge=1)
    percentual: float = Field(..., ge=0)


class ParcelamentoConfig(BaseModel):
    produto: str
    versao: int = Field(..., ge=1)
    parcelas: ParcelaRangeConfig
    juros_por_limite: list[JurosPorLimiteConfig]

    @model_validator(mode="after")
    def validar_tabela_juros(self) -> "ParcelamentoConfig":
        if not self.juros_por_limite:
            raise ValueError("tabela de juros nao pode ser vazia")

        ultimo_limite = 0
        for item in self.juros_por_limite:
            if item.limite_superior <= ultimo_limite:
                raise ValueError("limites da tabela de juros devem ser crescentes")
            ultimo_limite = item.limite_superior

        if self.juros_por_limite[-1].limite_superior != self.parcelas.maximo:
            raise ValueError("ultimo limite da tabela de juros deve cobrir o maximo de parcelas")

        return self


CONFIG_PATH = Path(__file__).resolve().parent / "config" / "parcelamento.v1.json"


@lru_cache
def get_parcelamento_config() -> ParcelamentoConfig:
    with CONFIG_PATH.open("r", encoding="utf-8") as config_file:
        raw_config = json.load(config_file)
    return ParcelamentoConfig.model_validate(raw_config)
