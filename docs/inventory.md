## Returns paginated inventory positions by store and SKU.

### Use cases:
- Monitor stock levels.
- Feed OMS, ERP, or e-commerce platforms.
- Support replenishment and planning.

### Filters:
- store_code (optional)
- page
- size

> If no `store_code` is provided, the API returns inventory positions for all stores in the database. Use the pagination parameters (`page` and `size`) to limit the number of inventory records returned in a single response.

### Returns:
- store_code - `string`
- cnpj - `string`
- sku - `string`
- product_stock_date - `date`
- product_stock_quantity - `integer`

### SKU Information: 
> A Stock Keeping Unit (SKU) is a unique alphanumeric code assigned to products by retailers to track inventory internally. SKUs identify specific product attributes like brand, style, color, and size (e.g., TSH-BLK-08 for a black T-shirt, size 8). Unlike universal barcodes, SKUs are customized by each company to manage stock, analyze sales trends, and improve warehouse efficiency.

### CNPJ Information:
- CNPJ stands for Cadastro Nacional da Pessoa Jurídica (National Registry of Legal Entities) in Brazil. It is a 14-digit, mandatory federal tax identification number (formatted XX.XXX.XXX/XXXX-XX) issued by the Brazilian Federal Revenue Service to companies, branches, and organizations for legal, tax, and commercial operations. It is used for tax reporting, invoicing, and legal identification of businesses in Brazil.
- To make it simple, the API returns only the digits of the `cnpj` without formatting.
- This column can serve as a unique identifier of an store.