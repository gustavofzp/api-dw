from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class EstoqueLojasParams(BaseModel):
    page: int = Field(..., ge=1, description="Número da página (mínimo 1)")
    size: int = Field(..., ge=1, le=1000, description="Tamanho da página (entre 1 e 1000)")
    loja_id: Optional[int] = Field(None, description="ID da loja (opcional)")


class ImagensProdutosParams(BaseModel):
    ref: str = Field(..., description="Referência do produto")
    cor: str = Field(..., description="Cor do produto")


class MovimentosLojasParams(BaseModel):
    start_date: date = Field(..., description="Data inicial no formato YYYY-MM-DD")
    end_date: date = Field(..., description="Data final no formato YYYY-MM-DD")
    page: int = Field(1, ge=1, description="Número da página (mínimo 1)")
    size: int = Field(500, ge=1, le=1000, description="Tamanho da página (entre 1 e 1000)")
    loja_id: Optional[int] = Field(None, description="ID da loja (opcional)")