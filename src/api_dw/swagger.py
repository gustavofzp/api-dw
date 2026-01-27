from fastapi.openapi.utils import get_openapi


def setup_swagger(app):
    app.title = "API DW"
    app.description = """
    API do Data Warehouse.

    Serviços disponíveis:
    - Estoque por loja
    - Imagens de produtos
    - Movimentos de lojas

    Todos os endpoints exigem autenticação via token com excessão do doecho.
    """
    app.version = "1.0.0"

    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema

        openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
        )

        # Swagger logo
        openapi_schema["info"]["x-logo"] = {
            "url": "/static/LIVE!TECH---PTO.png"
        }

        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi
