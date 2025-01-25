## Wishlist API Documentation

## Base url
wishlist/

1. Get Wishlist
URL: /wishlist/get-wishlist
Method: GET
Description: Retrieves all items in the authenticated user's wishlist, including products and services.

Authentication: JWT required.
Responses:
200:
If the wishlist contains items.
```json
{
  "wishlist": [
    {
      "id": "integer",
      "user_id": "integer",
      "product": {
        "id": "integer",
        "name": "string",
        "description": "string"
      },
      "service": {
        "id": "integer",
        "name": "string",
        "description": "string"
      }
    }
  ]
}
```

404:
If the user's wishlist is empty.
```json
{
  "message": "Your wishlist is empty."
}
```

2. Add to Wishlist
URL: /wishlist/add
Method: POST
Description: Adds a product or service to the authenticated user's wishlist.

Request Body:
```json
{
  "product_id": "integer",  // Product ID (optional)
  "service_id": "integer"   // Service ID (optional)
}
```

Authentication: JWT required.
Responses:
201:
On successful addition to the wishlist.
```json
{
  "message": "Product/Service added to your wishlist.",
  "wishlist_item": {
    "id": "integer",
    "user_id": "integer",
    "product": {
      "id": "integer",
      "name": "string",
      "description": "string"
    },
    "service": {
      "id": "integer",
      "name": "string",
      "description": "string"
    }
  }
}
```

400:
If neither product_id nor service_id is provided.
```json
{
  "message": "Either product_id or service_id must be provided."
}
```

3. Remove from Wishlist
URL: /wishlist/remove
Method: POST
Description: Removes a product or service from the authenticated user's wishlist.

Request Body:
```json
{
  "product_id": "integer",  // Product ID (optional)
  "service_id": "integer"   // Service ID (optional)
}
```

Authentication: JWT required.
Responses:
200:
On successful removal from the wishlist.
```json
{
  "message": "Product/Service removed from your wishlist."
}
```

400:
If neither product_id nor service_id is provided.
```json
{
  "message": "Either product_id or service_id must be provided."
}
```

404:
If the product or service is not found in the user's wishlist.
```json
{
  "message": "Product/Service not found in your wishlist."
}
```