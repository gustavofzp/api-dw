## Returns transactional movements for stores, including sales, exchanges, and cancellations.

### Filters:
- store_id (optional)
- start_date (optional)
- end_date (optional)
- page
- size

> If no `store_id` is provided, the API returns transactions for all stores in the database.
> if no `start_date` and `end_date` are provided, the API returns all transactions for the specified `store_id` (or all stores if `store_id` is not provided). Pagination parameters (`page` and `size`) can be used to limit the number of transactions returned in a single response.
> if a `start_date` are provided, but no `end_date` is provided, the API returns all transactions from the `start_date` to the most recent transaction available in the database. If an `end_date` is provided without a `start_date`, the API returns error.

### Returns:
- store_code - `string`
- cnpj - `string`
- sku - `string`
- product_stock_date - `Date`
- product_stock_quantity - `integer`

### CNPJ Information:
- CNPJ stands for Cadastro Nacional da Pessoa Jurídica (National Registry of Legal Entities) in Brazil. It is a 14-digit, mandatory federal tax identification number (formatted XX.XXX.XXX/XXXX-XX) issued by the Brazilian Federal Revenue Service to companies, branches, and organizations for legal, tax, and commercial operations. It is used for tax reporting, invoicing, and legal identification of businesses in Brazil.
- To make it simple, the API returns only the digits of the `cnpj` without formatting.
- This column can serve as a unique identifier of an store.
