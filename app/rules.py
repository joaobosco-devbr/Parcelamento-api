from functools import lru_cache
from typing import Final

from app.settings import get_parcelamento_config


@lru_cache
def _config():
    return get_parcelamento_config()


MIN_PARCELAS: Final[int] = _config().parcelas.minimo
MAX_PARCELAS: Final[int] = _config().parcelas.maximo
MENSAGEM_ERRO_PARCELAS_INVALIDAS: Final[str] = (
    f"parcelas deve estar entre {MIN_PARCELAS} e {MAX_PARCELAS}"
)

PARCELAS_PERMITIDAS: Final[tuple[int, ...]] = tuple(range(MIN_PARCELAS, MAX_PARCELAS + 1))


def parcelas_sao_validas(quantidade_parcelas: int) -> bool:
    return MIN_PARCELAS <= quantidade_parcelas <= MAX_PARCELAS


def obter_percentual_juros(quantidade_parcelas: int) -> float:
    if not parcelas_sao_validas(quantidade_parcelas):
        raise ValueError(MENSAGEM_ERRO_PARCELAS_INVALIDAS)

    for item in _config().juros_por_limite:
        if quantidade_parcelas <= item.limite_superior:
            return item.percentual

    raise ValueError(MENSAGEM_ERRO_PARCELAS_INVALIDAS)
