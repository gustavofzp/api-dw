with lojas as(
    select
        REPLACE('L' || TO_CHAR(loja.cod_portal,'000'), ' ', '') as cod_portal,
        loja.pk_loja as cod_loja,
        loja.pk_cnpj as cnpj,
        loja.desc_apelido as nome_loja,
        loja.cod_rede,
        loja.rede
    from live.dlojas loja
    where loja.cod_rede in (7,8)
)
select
    lojas.cod_portal,
    lojas.cod_loja,
    lojas.cnpj,
    lojas.nome_loja,
    estoque.cnpj,
    estoque.fantasia as Nome_loja,
    estoque.data_estoque as data_estoque,
    estoque.sku,
    estoque.qtd_estoque as Qtde_Estoque
from estoque.fsaldoestoqueinteg estoque
    inner join lojas
        on lojas.cnpj = REGEXP_REPLACE(estoque.cnpj, '[^0-9]+', '', 'g')
        and lojas.cod_portal = estoque.loja
        and estoque.rede in ('PRÓPRIA', 'OUTLET')
where 1=1
    and estoque.data_estoque = (select max(estoque2.data_estoque) from estoque.fsaldoestoqueinteg estoque2)
    and estoque.qtd_estoque !=0
    and estoque.situacao = '1'
    --and lojas.cod_portal =
--LIMIT <page> OFFSET <size>