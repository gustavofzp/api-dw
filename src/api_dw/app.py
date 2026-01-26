import os
import src.api_dw.get_dados as get_dados
import src.api_dw.authentication as auth
import src.api_dw.validacao_parametros as vp

from fastapi import FastAPI, Query, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/test_token")
async def protected_route(token: str = Depends(auth.verify_token)):
    return {"mensagem": "Acesso concedido", "token": "ok"}


@app.get("/doecho")
async def doecho(msg: str = Query(default=None, max_length=50)):
    item = {
            "Method": "doecho", 
            "Status": "Sucess", 
            "Message": msg
    }
    content = jsonable_encoder(item)
    return JSONResponse(content=content)


@app.get("/estoque_lojas")
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


@app.get("/imagens_produtos")
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
    

@app.get("/movimentos_lojas")
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