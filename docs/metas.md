## Returns sales targets for stores per day.

### Filters:
- cnpj (optional)
- store_code (optional)
- target_date (optional) - (format: YYYY-MM-DD)
- page
- size

### Returns:
- cnpj - `string`
- store_code - `string`
- target_date - `Date`
- sales_target - `float` 

> sales_target is a monetary value representing the sales target for the store on the specified date.

### CNPJ Information:
- CNPJ stands for Cadastro Nacional da Pessoa Jurídica (National Registry of Legal Entities) in Brazil. It is a 14-digit, mandatory federal tax identification number (formatted XX.XXX.XXX/XXXX-XX) issued by the Brazilian Federal Revenue Service to companies, branches, and organizations for legal, tax, and commercial operations. It is used for tax reporting, invoicing, and legal identification of businesses in Brazil.
- To make it simple, the API returns only the digits of the `cnpj` without formatting.
- This column can serve as a unique identifier of an store.