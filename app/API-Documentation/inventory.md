## Inventory API Docmentation

## Base url
/inventory

1. Add Inventory
URL: /inventory/add
Method: POST
Description: Adds a new inventory entry.

Request Body:
```json
{
  "product_id": "integer",  // The ID of the product
  "service_id": "integer",  // The ID of the service
  "stock": "integer"  // The stock quantity
}
```

Responses:
400:
If any of the required fields are missing.
Example:
```json
{ "error": "Missing required fields" }
```

201:
On successful inventory creation.
Example:
```json
{ "result": "success_message" }
```

2. Get Inventory by ID
URL: /inventory/<inventory_id>
Method: GET
Description: Retrieves an inventory record by its ID.
URL Parameters:
inventory_id: The ID of the inventory record.

Responses:
200:
If the inventory record is found.
Example:
```json
{
  "id": "integer",
  "product_id": "integer",
  "service_id": "integer",
  "stock": "integer",
  "last_updated": "string"
}
```

404:
If the inventory ID is not found.
Example:
```json
{ "error": "Inventory record not found" }
```

3. Get All Inventory
URL: /inventory/
Method: GET
Description: Retrieves all inventory records.

Responses:
200:
If inventory records are found.
Example:
```json
[
  {
    "id": "integer",
    "product_id": "integer",
    "service_id": "integer",
    "stock": "integer",
    "last_updated": "string"
  },
  ...
]
```


4. Update Inventory Stock
URL: /inventory/update/<inventory_id>
Method: PUT
Description: Updates the stock quantity of an inventory record.
URL Parameters:
inventory_id: The ID of the inventory record to update.

Request Body:
```json
{
  "stock": "integer"  // New stock value
}
```

Responses:
400:
If the stock value is missing.
Example:
```json
{ "error": "Stock value is required" }
```

200:
On successful stock update.
Example:
```json
{ "result": "success_message" }
```

5. Delete Inventory
URL: /inventory/delete/<inventory_id>
Method: DELETE
Description: Deletes an inventory record by its ID.
URL Parameters:
inventory_id: The ID of the inventory record to delete.

Responses:
200:
On successful deletion.
Example:
```json
{ "result": "Inventory record deleted" }
```