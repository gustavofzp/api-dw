import os
import src.api_dw.get_dados as get_dados
import src.api_dw.authentication as auth
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
    tags=["Autenticação"],
    summary="Verifica token",
    description="Endpoint simples para verificar se o token de autenticação é válido."
)
async def protected_route(token: str = Security(security)):
    auth.verify_token(token.credentials)
    return {"mensagem": "Acesso concedido", "token": "ok"}



@app.get(
    "/doecho",
    tags=["Util"],
    summary="Echo de teste",
    description="Endpoint simples para teste de conectividade."
)
async def doecho(msg: str = Query(default=None, max_length=50)):
    item = {
            "Method": "doecho", 
            "Status": "Sucess", 
            "Message": msg
    }
    content = jsonable_encoder(item)
    return JSONResponse(content=content)



@app.get(
    "/estoque_lojas",
    tags=["Estoque"],
    summary="Consulta estoque das lojas",
    description="Retorna o estoque paginado por loja e produto."
)
async def estoque_lojas(
    params: vp.EstoqueLojasParams = Depends(),
    token: str = Depends(auth.verify_token)  # Adiciona a verificação do token como dependência
):
    try:
        dados = get_dados.dados_estoque(params.page, params.size, params.loja_id)

        if not dados:
            raise HTTPException(status_code=404, detail="Loja não encontrada")
        
        # Define os cabeçalhos
        headers = ["cod_portal", "cod_loja", "cnpj_loja", "nome_loja", "cnpj", "nome_loja", "data_estoque", "sku", "qtde_estoque"]

        # Transforma os dados em uma lista de dicionários
        dados = [dict(zip(headers, linha)) for linha in dados]
        item = {
            "Method": "estoque_lojas", 
            "Status": "Sucess", 
            "Data": dados
        }
        content = jsonable_encoder(item)
        return JSONResponse(content=content)
    except Exception as e:
        item = {
            "Method": "estoque_lojas", 
            "erro": str(e)
        }
        content = jsonable_encoder(item)
        return JSONResponse(content=content)



@app.get(
    "/imagens_produtos",
    tags=["Produtos"],
    summary="Consulta imagens dos produtos",
    description="Retorna URLs das imagens por referência e cor."
)
async def imagens_produtos(
    params: vp.ImagensProdutosParams = Depends(),
    token: str = Depends(auth.verify_token)
):
    try:
        dados = get_dados.dados_img(params.ref, params.cor)

        if not dados:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        
        # Define os cabeçalhos
        headers = ["id_produto", "ref", "cor", "seq_imagem", "imagem_url"]
        # Transforma os dados em uma lista de dicionários
        dados = [dict(zip(headers, linha)) for linha in dados]        
        
        item = {
            "Method": "imagens_produtos", 
            "Status": "Sucess",
            "Data": dados
        }
        content = jsonable_encoder(item)
        return JSONResponse(content=content)
    except Exception as e:
        item = {
            "Method": "imagens_produtos", 
            "erro": str(e)
        }
        content = jsonable_encoder(item)
        return JSONResponse(content=content)
    


@app.get(
    "/movimentos_lojas",
    tags=["Movimentos"],
    summary="Consulta movimentos das lojas",
    description="Retorna vendas, trocas e cancelamentos por período."
)
async def movimentos_lojas(
    params: vp.MovimentosLojasParams = Depends(),
    token: str = Depends(auth.verify_token)    
):
    try:
        dados = get_dados.dados_movimentos(params.start_date, params.end_date, params.page, params.size, params.loja_id)

        if not dados:
            raise HTTPException(status_code=404, detail="Loja não encontrada")
        
        # Define os cabeçalhos
        headers = ["cod_portal", "cod_loja", "cnpj", "nome_loja", "data_lancamento", "canal_distribuicao", "fk_produto",
                   "cod_barra", "cor", "tamanho", "cancelado", "datcancel", "desc_movimento", "operacao", "rede", "serie",
                   "numnf", "cod_vendedor", "considerarvenda", "situacao", "qtde", "valor_liquido", "desconto"]
        # Transforma os dados em uma lista de dicionários
        dados = [dict(zip(headers, linha)) for linha in dados]
        item = {
            "Method": "movimentos_lojas", 
            "Status": "Sucess", 
            "Data": dados
        }
        content = jsonable_encoder(item)
        return JSONResponse(content=content)
    except Exception as e:
        item = {
            "Method": "movimentos_lojas", 
            "erro": str(e)
        }
        content = jsonable_encoder(item)
        return JSONResponse(content=content)