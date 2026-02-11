select
    prod.sku_produto as sku,
    prod.pk_produto_cigam as erp_product_code,
    prod.cd_referencia || prod.cd_cor as Style_Color_Code,
    prod.desc_produto as description,
    prod.cd_referencia as style_code,
    prod.cd_cor as color_code,
    prod.nm_cor as color_name,
    prod.cd_tamanho as size_code,
    prod.nm_tamanho as size_name,
    prod.cod_linha as product_line_code,
    prod.linha_produto as product_line_name,
    prod.cod_agrupador as category_code,
    prod.desc_agrupador as category_name,
    prod.cod_artigo as product_type_code,
    prod.desc_artigo as product_type_name,
    prod.cd_colecao as collection_code,
    prod.desc_colecao as collection_name,
    prod.cod_subcolecao as sub_collection_code,
    prod.desc_sub_colecao as sub_collection_name,
    prod.item_ativo as is_active
from live.dproduto prod
where prod.nivel_estrutura = 1
    --and prd.sku
    --and prd.ativo =
--LIMIT <page> OFFSET <size>