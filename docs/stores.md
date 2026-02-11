## Returns detailed information about physical and digital stores.

### Use cases:
- Synchronize store master data.
- Load store dimensions in BI and DW layers.
- Validate operational store metadata.

### Filters:
- `store_code` (optional)

> If no `store_code` is provided, the API returns all stores in the database.

### Returns:
- store_code - `string`
- cnpj  `string`
- store_name -  `string`
- store_chain_code - `integer`
- store_chain_name - `string`
- zip_code - `integer`
- address - `string`
- city_code - `integer`
- city_name - `string`
- state  - `string`
- region_code - `integer`
- region_name - `string`
- store_size - `string`
- opening_date - `Date`
- is_open_sunday - `integer`  (0 or 1)

### CNPJ Information:
- CNPJ stands for Cadastro Nacional da Pessoa Jurídica (National Registry of Legal Entities) in Brazil. It is a 14-digit, mandatory > . federal tax identification number (formatted XX.XXX.XXX/XXXX-XX) issued by the Brazilian Federal Revenue Service to companies, branches, and organizations for legal, tax, and commercial operations. It is used for tax reporting, invoicing, and legal identification of businesses in Brazil.
- To make it simple, the API returns only the digits of the `cnpj` without formatting.
- This column can serve as a unique identifier of an store.