## Returns detailed information about physical and digital stores.

### Use cases:
- Synchronize store master data.
- Load store dimensions in BI and DW layers.
- Validate operational store metadata.

### Filters:
- `store_id` (optional)

> If no `store_id` is provided, the API returns all stores in the database.

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
- is_open_sunday - `integer`
- is_active - `integer`

### CNPJ Information:
- CNPJ stands for Cadastro Nacional da Pessoa Jurídica (National Registry of Legal Entities) in Brazil. It is a 14-digit, mandatory > . federal tax identification number (formatted XX.XXX.XXX/XXXX-XX) issued by the Brazilian Federal Revenue Service to companies, branches, and organizations for legal, tax, and commercial operations. It is used for tax reporting, invoicing, and legal identification of businesses in Brazil.
- To make it simple, the API returns only the digits of the `cnpj` without formatting.
- This column can serve as a unique identifier of an store.

### is_ columns information:
> The `is_` columns (e.g., `is_open_sunday`, `is_active`) are binary indicators where `1` represents "Yes" or "True" and `0` represents "No" or "False".
> For example, if `is_open_sunday` is `1`, it means the store is open on Sundays; if it is `0`, the store is closed on Sundays. 
> Similarly, if `is_active` is `1`, the store is currently active, while `0` indicates that the store is inactive.