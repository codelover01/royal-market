## API Documentation for Product Management

1. Add a Product
**Endpoint:** `/products/add_products`
**Method:** `POST`
Description: Adds a product to the database for a specific business owned by the current user.

Request Body:

business_id (int, required): The ID of the business to which the product belongs.
name (str, required): The name of the product.
description (str, optional): A description of the product.
price (float, required): The price of the product.
quantity (int, required): The quantity of the product being added.
stock (int, optional): The stock availability for the product.

Responses:
201: Product added successfully.
```json
{
    "message": "Product added successfully",
    "product": { "id": int, "name": str, "description": str, "price": float, "quantity": int, ... }
}
```

400: Invalid JSON or missing business_id.
```json
{"error": "Invalid JSON"}
```json
{"error": "Business ID is required."}
```

403: User owns no businesses or business_id is invalid.
```json
{"error": "You do not own any business"}
```json
{"error": "Invalid business ID or you do not own this business."}
```

500: Internal server error.
```json
{"error": "Detailed error message"}
```


2. List All Products
Endpoint: /products/list_products
Method: GET
Description: Retrieves all products from the database.

Responses:

200: List of all products.
```json
{
    "products": [
        {"id": int, "name": str, "description": str, "price": float, "quantity": int, ... },
        ...
    ]
}
```

500: Internal server error.
```json
{"error": "Detailed error message"}
```

3. Delete a Product
Endpoint: /products/delete_products/<product_id>
Method: POST or DELETE
Description: Deletes a specific product by ID if it belongs to a business owned by the current user.

Path Parameter:
product_id (int, required): The ID of the product to delete.
Responses:

200: Product deleted successfully.
```json
{"message": "Product deleted successfully"}
```

403: Product does not belong to the user's business.
```json
{"error": "Unauthorized: You do not own this product."}
```

500: Internal server error.
```json
{"error": "Detailed error message"}
```