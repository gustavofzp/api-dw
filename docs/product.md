## Returns the product master catalog with SKU, style, color, size, and collection attributes.

### Use cases:
- Build product dimensions.
- Integrate with marketplaces and e-commerce.
- Support pricing, stock, and imagery joins.

### Filters:
- sku (optional)
- is_active (optional)
- page
- size

> - If no `sku` is provided, the API returns all products in the database.
> - If `is_active` is provided, the API filters products based on their active status (1 for active, 0 for inactive). 
> In both cases, use the pagination parameters (`page` and `size`) can limit the number of products returned in a single response.

### Returns:
- sku - `string`
- erp_product_code - `string`
- Style_Color_Code - `string`
- description - `string`
- style_code - `string`
- color_code - `string`
- color_name - `string`
- size_code - `string`
- size_name - `string`
- product_line_code - `integer`
- product_line_name - `string`
- category_code - `integer`
- category_name - `string`
- product_type_code - `integer`
- product_type_name - `string`
- collection_code - `integer`
- collection_name - `string`
- sub_collection_code - `integer`
- sub_collection_name - `string`
- is_active - `integer`

### SKU Information: 
> A Stock Keeping Unit (SKU) is a unique alphanumeric code assigned to products by retailers to track inventory internally. SKUs identify specific product attributes like brand, style, color, and size (e.g., TSH-BLK-08 for a black T-shirt, size 8). Unlike universal barcodes, SKUs are customized by each company to manage stock, analyze sales trends, and improve warehouse efficiency.

### is_active Information:
> The `is_active` column is a binary indicator where `1` represents "Yes" or "True" and `0` represents "No" or "False". For example, if `is_active` is `1`, it means the product is currently active and available for sale; if it is `0`, the product is inactive, which could indicate it is discontinued, out of stock, or not currently offered for sale.