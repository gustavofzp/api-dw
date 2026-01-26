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
    mov.data_lancamento,
    mov.canal_distribuicao,
    mov.fk_produto,
    mov.cod_barra,
    mov.cor,
    mov.tamanho,
    mov.cancelado,
    mov.datcancel,
    mov.desc_movimento,
    mov.operacao,
    mov.rede,
    mov.serie,
    mov.numnf,
    mov.cod_vendedor,
    mov.considerarvenda,
    mov.situacao,
    mov.qtde,
    mov.valor_liquido,
    mov.desconto
from jma.fmovimentosinteg mov
    inner join lojas
        on lojas.cnpj = mov.cnpj
where 1=1
    --and mov.data_lancamento between
    --and lojas.cod_portal =
LIMIT 10 OFFSET 0