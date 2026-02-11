with lojas as(
    select
        REPLACE('L' || LPAD(loja.cod_portal::text, 3, '0'), ' ', '') as cod_portal,
        loja.pk_cnpj as cnpj,
        loja.cod_rede,
        loja.rede
    from live.dlojas loja
    where loja.cod_rede in (7,8)
)
select
    lojas.cod_portal as store_code,
    lojas.cnpj,
    estoque.sku,
    estoque.data_estoque as product_stock_date,
    estoque.qtd_estoque as product_stock_quantity
from estoque.fsaldoestoqueinteg estoque
    inner join lojas
        on lojas.cnpj = REGEXP_REPLACE(estoque.cnpj, '[^0-9]+', '', 'g')
        and lojas.cod_portal = estoque.loja
where 1=1
    and estoque.data_estoque = (select max(estoque2.data_estoque) from estoque.fsaldoestoqueinteg estoque2)
    and estoque.qtd_estoque <> 0
    and estoque.situacao = '1'
    --and lojas.cod_portal =
--LIMIT <page> OFFSET <size>