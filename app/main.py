from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.routers.health import router as health_router
from app.routers.simulacao import router as simulacao_router


API_V1_PREFIX = "/api/v1"


app = FastAPI(
    title="API de Simulacao de Parcelamento",
    description=(
        "API REST versionada para simulacao de parcelamento com regras "
        "versionadas de juros por quantidade de parcelas."
    ),
    version="1.0.0",
)


@app.exception_handler(RequestValidationError)
def handle_request_validation_error(_: Request, exc: RequestValidationError) -> JSONResponse:
    details = []
    for error in exc.errors():
        location = [str(item) for item in error["loc"] if item != "body"]
        details.append(
            {
                "field": ".".join(location) if location else "request",
                "message": error["msg"],
            }
        )

    return JSONResponse(
        status_code=422,
        content={
            "code": "validation_error",
            "message": "Dados de entrada invalidos",
            "details": details,
        },
    )


@app.exception_handler(ValueError)
def handle_value_error(_: Request, exc: ValueError) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={
            "code": "business_rule_error",
            "message": "Regra de negocio violada",
            "details": [
                {
                    "field": "request",
                    "message": str(exc),
                }
            ],
        },
    )


app.include_router(health_router, prefix=API_V1_PREFIX)
app.include_router(simulacao_router, prefix=API_V1_PREFIX)
