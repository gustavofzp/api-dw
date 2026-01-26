select
    img_prd.id_produto,
    img_prd.referencia,
    img_prd.cor,
    img_prd.seq_imagem,
    img_prd.imagem_url 
from live.dimg_produtos img_prd
where 1=1
--    and img_prd.referencia = 
--    and img_prd.cor =
--    and img_prd.id_produto =