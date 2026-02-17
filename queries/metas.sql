select
    loj.pk_cnpj as cnpj,
    REPLACE('L' || LPAD(loj.cod_portal::text, 3, '0'), ' ', '') as store_code,
    meta.dt_meta::date as target_date,
    meta.valor_meta as target_value
from jma.fmeta_diario_loja meta
    inner join live.dlojas loj
        on loj.pk_loja = meta.cod_loja
        and loj.cod_rede in (6, 12, 7, 18, 8, 36)
where 1=1
    and meta.dt_meta >= TO_DATE('2026-01-01','YYYY/MM/DD')
    -- loj.pk_cnpj =
    -- loj.cod_portal =
--LIMIT <page> OFFSET <size>