## Returns product images by style and color.

### Filters:
- style_code
- color_code

### Returns:
- style_color_code - `string`
- style_code - `string`
- color_code - `string`
- image_sequence - `integer`
- image_url - `string`

### image_sequence Information:
> The `image_sequence` column indicates the order of images for a specific style and color combination. It´s the same images of our ecommerce, so the image with `image_sequence` equal to `1` is the main image for that style and color, while images with higher `image_sequence` values are additional images showing different angles or details of the product. This allows users to easily identify and display the primary image for a product while also providing access to supplementary images for a more comprehensive view.