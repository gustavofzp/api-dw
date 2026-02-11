The Live! API provides structured, secure, and scalable access to Live!’s data warehouse, enabling integrations with partners, internal services, analytics platforms, and operational systems.

It exposes standardized endpoints for products, stores, inventory, images, and transactional movements with pagination, filtering, and authentication support.


## Base Information

- **Version:** v1  
- **Format:** JSON  
- **Authentication:** Bearer Token  
- **Pagination:** Supported on large datasets  
- **Timezone:** UTC-3 (unless stated otherwise)

All protected endpoints require a valid token passed via the `Authorization` header:

```http
Authorization: Bearer <your_token_here>
