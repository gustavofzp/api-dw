from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class EstoqueLojasParams(BaseModel):
    page: int = Field(..., ge=1, description="Page number (minimum 1)")
    size: int = Field(..., ge=1, le=1000, description="Page size (between 1 and 1000)")
    cnpj: Optional[str] = Field(None, description="Store CNPJ (optional)")
    store_code: Optional[str] = Field(None, description="Store code (optional)")
    product_stock_date: Optional[date] = Field(None, description="Stock date in YYYY-MM-DD format (optional)")
    sku: Optional[str] = Field(None, description="Product SKU (optional)")



class ImagensProdutosParams(BaseModel):
    style_code: str = Field(..., description="Product reference code")
    color_code: str = Field(..., description="Product color code")



class MovimentosLojasParams(BaseModel):
    cnpj: Optional[str] = Field(None, description="Store CNPJ (optional)")
    store_code: Optional[str] = Field(None, description="Store code (optional)")
    start_date: Optional[date] = Field(None, description="Start date in YYYY-MM-DD format (optional)")
    end_date: Optional[date] = Field(None, description="End date in YYYY-MM-DD format (optional)")
    page: int = Field(1, ge=1, description="Page number (minimum 1)")
    size: int = Field(500, ge=1, le=1000, description="Page size (between 1 and 1000)")



class ProductParams(BaseModel):
    sku: Optional[str] = Field(None, description="Product SKU (optional)")
    is_active: Optional[int] = Field(None, description="Product active status (optional)")
    page: int = Field(1, ge=1, description="Page number (minimum 1)")
    size: int = Field(500, ge=1, le=1000, description="Page size (between 1 and 1000)")



class lojasParams(BaseModel):
    page: int = Field(1, ge=1, description="Page number (minimum 1)")
    size: int = Field(500, ge=1, le=1000, description="Page size (between 1 and 1000)")
    cnpj: Optional[str] = Field(None, description="Store CNPJ (optional)")
    store_code: Optional[str] = Field(None, description="Store code (optional)")



class metasParams(BaseModel):
    page: int = Field(1, ge=1, description="Page number (minimum 1)")
    size: int = Field(500, ge=1, le=1000, description="Page size (between 1 and 1000)")
    cnpj: Optional[str] = Field(None, description="Store CNPJ (optional)")
    store_code: Optional[str] = Field(None, description="Store code (optional)")
    target_date: Optional[date] = Field(None, description="Target date in YYYY-MM-DD format (optional)")