select
    img_prd.id_produto  as style_color_code,
    img_prd.referencia  as style_code,
    img_prd.cor         as color_code,
    img_prd.seq_imagem  as image_sequence,
    img_prd.imagem_url  as image_url
from live.dimg_produtos img_prd
where 1=1
    and img_prd.seq_imagem = 1
--    and img_prd.referencia = 
--    and img_prd.cor =
