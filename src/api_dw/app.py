import os
import json
import textwrap
import src.api_dw.get_dados as get_dados
import src.api_dw.authentication as auth
import src.api_dw.tradutor as tradutor
import src.api_dw.validacao_parametros as vp

from fastapi import FastAPI, Query, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBearer
from fastapi import Security
from fastapi.openapi.docs import get_swagger_ui_html
from .swagger import setup_swagger
from dotenv import load_dotenv

load_dotenv()
app = FastAPI(docs_url="/docs", redoc_url="/redoc")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
security = HTTPBearer()
app.mount("/static", StaticFiles(directory="src/api_dw/static"), name="static")
setup_swagger(app)

BASE_DIR = os.path.dirname(__file__)
with open(os.path.join(BASE_DIR, "..", "..", "docs", "swagger_responses.json"), encoding="utf-8") as f:
    SWAGGER_RESPONSES = json.load(f)



def le_descricao(arquivo):
    from pathlib import Path
    docs_dir = Path(__file__).resolve().parent.parent.parent / "docs"
    arquivo_path = docs_dir / arquivo

    if not arquivo_path.exists():
        available = sorted([p.name for p in docs_dir.glob("*.md")]) if docs_dir.exists() else []
        raise FileNotFoundError(
            f"Description file not found: {arquivo_path}\n"
            f"Docs directory: {docs_dir}\n"
            f"Available files: {available}"
        )

    with arquivo_path.open("r", encoding="utf-8") as f:
        texto = f.read()

    texto = texto.replace("\r\n", "\n")
    texto = textwrap.dedent(texto).strip()
    return texto



@app.get("/docs", include_in_schema=False)
def custom_docs():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title="API DW - Docs",
        swagger_css_url="/static/swagger.css",
        swagger_ui_parameters={
            "filter": True,
            "displayRequestDuration": True,
            "persistAuthorization": True
        }
    )



@app.get(
    "/test_token",
    tags=["Utility"],
    summary="Verify token",
    description="Simple endpoint to check if the authentication token is valid."
)
async def protected_route(token: str = Security(security)):
    auth.verify_token(token.credentials)
    return {"message": "Access granted", "token": "ok"}



@app.get(
    "/doecho",
    tags=["Utility"],
    summary="Test echo",
    description="Simple endpoint for connectivity testing."
)
async def doecho(msg: str = Query(default=None, max_length=50)):
    item = {
            "Method": "doecho", 
            "Status": "Success", 
            "Message": msg
    }
    content = jsonable_encoder(item)
    return JSONResponse(content=content)



@app.get(
    "/store_inventory",
    tags=["Stores"],
    summary="Query store inventory",
    description= le_descricao(arquivo="inventory.md"),
    responses={
        200: SWAGGER_RESPONSES["store_inventory"]["200"],
        401: {"description": "Unauthorized"},
        404: {"description": "Store not found"}
    }
)
async def store_inventory(
    params: vp.EstoqueLojasParams = Depends(),
    token: str = Depends(auth.verify_token)  # Adds token verification as dependency
):
    try:
        dados = get_dados.dados_estoque(params.page, params.size, params.store_code)

        if not dados:
            raise HTTPException(status_code=404, detail="Store not found")

        content = jsonable_encoder(dados)
        return JSONResponse(content=content)
    except Exception as e:
        item = {
            "Method": "store_inventory", 
            "error": str(e)
        }
        content = jsonable_encoder(item)
        return JSONResponse(content=content)



@app.get(
    "/product_images",
    tags=["Product"],
    summary="Query product images",
    description= le_descricao(arquivo="prd_images.md"),
    responses={
        200: SWAGGER_RESPONSES["product_images"]["200"],
        401: {"description": "Unauthorized"},
        404: {"description": "Product not found"}
    }
)
async def product_images(
    params: vp.ImagensProdutosParams = Depends(),
    token: str = Depends(auth.verify_token)
):
    try:
        dados = get_dados.dados_img(params.style_code, params.color_code)
        if not dados:
            raise HTTPException(status_code=404, detail="Product not found")
        
        # Define headers
        headers = ["style_color_code","style_code","color_code","image_sequence","image_url"]
        dados = tradutor.ensure_records(dados, headers)
        item = {
            "Method": "product_images", 
            "Status": "Success",
            "Data": dados
        }
        content = jsonable_encoder(item)
        return JSONResponse(content=content)
    except Exception as e:
        item = {
            "Method": "product_images", 
            "error": str(e)
        }
        content = jsonable_encoder(item)
        return JSONResponse(content=content)



@app.get(
    "/store_transactions",
    tags=["Stores"],
    summary="Query store transactions",
    description= le_descricao(arquivo="transactions.md"),
    responses={
        200: SWAGGER_RESPONSES["store_transactions"]["200"],
        401: {"description": "Unauthorized"},
        404: {"description": "Transactions not found"}
    }
)
async def store_transactions(
    params: vp.MovimentosLojasParams = Depends(),
    token: str = Depends(auth.verify_token)    
):
    try:
        dados = get_dados.dados_movimentos(params.store_code, params.start_date, params.end_date, params.page, params.size)

        if not dados:
            raise HTTPException(status_code=404, detail="Transactions not found")

        content = jsonable_encoder(dados)
        return JSONResponse(content=content)
    except Exception as e:
        item = {
            "Method": "store_transactions", 
            "error": str(e)
        }
        content = jsonable_encoder(item)
        return JSONResponse(content=content)



@app.get(
    "/stores",
    tags=["Stores"],
    summary="Details of each store",
    description= le_descricao(arquivo="stores.md"),
    responses={
        200: SWAGGER_RESPONSES["stores"]["200"],
        401: {"description": "Unauthorized"},
        404: {"description": "No product found"}
    }
)
async def stores(
    params: vp.lojasParams = Depends(),
    token: str = Depends(auth.verify_token)
):
    try:
        dados = get_dados.dados_lojas(params.store_code)
        if not dados:
            raise HTTPException(status_code=404, detail="No store found")

        content = jsonable_encoder(dados)
        return JSONResponse(content=content)
    except Exception as e:
        item = {
            "Method": "stores", 
            "error": str(e)
        }
        content = jsonable_encoder(item)
        return JSONResponse(content=content)
    


@app.get(
    "/product_catalog",
    tags=["Product"],
    summary="Details of each product",
    description= le_descricao(arquivo="product.md"),
    responses={
        200: SWAGGER_RESPONSES["product_catalog"]["200"],
        401: {"description": "Unauthorized"},
        404: {"description": "No product found"}
    }
)
async def product_catalog(
    params: vp.ProductParams = Depends(),
    token: str = Depends(auth.verify_token)
):
    try:
        dados = get_dados.dados_produtos(params.sku, params.is_active, params.page, params.size)
        if not dados:
            raise HTTPException(status_code=404, detail="No product found")

        content = jsonable_encoder(dados)
        return JSONResponse(content=content)
    except Exception as e:
        item = {
            "Method": "product_catalog", 
            "error": str(e)
        }
        content = jsonable_encoder(item)
        return JSONResponse(content=content)