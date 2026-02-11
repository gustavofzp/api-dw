import os
import textwrap
from fastapi.openapi.utils import get_openapi


def le_arquivo(arquivo):
    caminho = os.path.join(os.path.dirname(__file__), "..", "..", arquivo)
    with open(caminho, "r", encoding="utf-8") as f:
        texto = f.read()
    texto = texto.replace("\r\n", "\n")
    texto = textwrap.dedent(texto).strip()
    return texto



def setup_swagger(app):
    app.title = "Live! API"
    app.description = le_arquivo(arquivo="docs/api_description.md")
    app.version = "1.2.0"

    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema

        openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
        )

        # Logo
        openapi_schema["info"]["x-logo"] = {
            "url": "/static/LIVE!TECH---PTO.png"
        }

        # Contact
        openapi_schema["info"]["contact"] = {
            "name": "Live! Tech",
            "email": "gustavo.puchalski@liveoficial.com.br"
        }

        # Security scheme
        openapi_schema["components"] = openapi_schema.get("components", {})
        openapi_schema["components"]["securitySchemes"] = {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT"
            }
        }

        # Apply globally
        openapi_schema["security"] = [
            {"BearerAuth": []}
        ]

        # Server example
        openapi_schema["servers"] = [
            {"url": "/", "description": "Default environment"}
        ]

        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi