select
    'L' || loj.cod_portal as store_code,
    loj.pk_cnpj as cnpj,
    loj.desc_apelido as store_name,
    loj.cod_rede as store_chain_code,
    loj.rede as store_chain_name,
    loj.cep as zip_code,
    loj.desc_endereco as address,
    loj.cod_cidade as city_code,
    loj.cidade as city_name,
    loj.estado as state,
    loj.cod_regiao as region_code,
    loj.regiao region_name,
    loj.metragem as store_size,
    loj.dt_inauguracao as opening_date,
    loj.flag_abre_aos_domingos as is_open_sunday
from live.dlojas loj
where 1=1
    AND loj.cod_rede IN (6, 12, 7, 18, 8, 36)
    and loj.situacao = 'ativo'
    --and lojas.cod_portal =
    --and prd.sku =
    --and prd.ativo =
--LIMIT <page> OFFSET <size>