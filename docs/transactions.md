## Returns transactional movements for stores, including sales, exchanges, and cancellations.

### Filters:
- store_code (optional)
- start_date (optional) - (format: YYYY-MM-DD)
- end_date (optional) - (format: YYYY-MM-DD)
- page
- size

> If no `store_code` is provided, the API returns transactions for all stores in the database.
> if no `start_date` and `end_date` are provided, the API returns all transactions for the specified `store_code` (or all stores if `store_code` is not provided). Pagination parameters (`page` and `size`) can be used to limit the number of transactions returned in a single response.
> if a `start_date` are provided, but no `end_date` is provided, the API returns all transactions from the `start_date` to the most recent transaction available in the database. If an `end_date` is provided without a `start_date`, the API returns error.

### Returns:
- store_code - `string`
- cnpj - `string`
- sku - `string`
- product_stock_date - `Date`
- product_stock_quantity - `integer`

- store_code  - `string`
- cnpj  - `string`
- store_name  - `string`
- transaction_date - `Date`
- sku  - `string`
- color_code  - `string`
- size_code  - `string`
- is_canceled  - `integer` (0 or 1)
- canceled_date - `Date` (null if not canceled)
- movement_description  - `string`
- operation  - `string`
- transaction_type - `string`
- invoice_series - `char`
- invoice_number - `integer`
- seller_code - `integer`
- is_sale - `integer` (0 or 1)
- movement_status - - `integer` 
- quantity - `integer`
- net_amount - `float`
- discount_amount - `float` 
- gross_amount - `float`

### CNPJ Information:
- CNPJ stands for Cadastro Nacional da Pessoa Jurídica (National Registry of Legal Entities) in Brazil. It is a 14-digit, mandatory federal tax identification number (formatted XX.XXX.XXX/XXXX-XX) issued by the Brazilian Federal Revenue Service to companies, branches, and organizations for legal, tax, and commercial operations. It is used for tax reporting, invoicing, and legal identification of businesses in Brazil.
- To make it simple, the API returns only the digits of the `cnpj` without formatting.
- This column can serve as a unique identifier of an store.
