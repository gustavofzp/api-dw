with lojas as(
    select
        REPLACE('L' || LPAD(loja.cod_portal::text, 3, '0'), ' ', '') as cod_portal,
        loja.pk_loja as cod_loja,
        loja.pk_cnpj as cnpj,
        loja.desc_apelido as nome_loja,
        loja.cod_rede,
        loja.rede
    from live.dlojas loja
    where loja.cod_rede in (7,8)
)
select
    lojas.cod_portal as store_code,
    lojas.cnpj,
    lojas.nome_loja as store_name,
    mov.data_lancamento as transaction_date,
    split_part(mov.fk_produto, '-', 4) || '.' ||
    split_part(mov.fk_produto, '-', 1) || '.' ||
    split_part(mov.fk_produto, '-', 2) || '.' ||
    split_part(mov.fk_produto, '-', 3) AS sku,
    mov.cor as color_code,
    mov.tamanho as size_code,
    case 
       when mov.cancelado = 'N' then 0
       else 1
    end as is_canceled,
    mov.datcancel as canceled_date,
    mov.desc_movimento as movement_description,
    mov.operacao as operation,
    mov.tipo_transacao as transaction_type,
    mov.serie as invoice_series,
    mov.numnf as invoice_number,
    mov.cod_vendedor as seller_code,
    case 
       when mov.considerarvenda = 'N' then 0
       else 1
    end as is_sale,
    mov.situacao as movement_status,
    mov.qtde as quantity,
    mov.valor_liquido as net_amount,
    mov.desconto as discount_amount,
    mov.valor_bruto as gross_amount
from jma.fmovimentosinteg mov
    inner join lojas
        on lojas.cnpj = mov.cnpj
where 1=1
    --and mov.data_lancamento between
    --and lojas.cod_portal =
LIMIT 10 OFFSET 0