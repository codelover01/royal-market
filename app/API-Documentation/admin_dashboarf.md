## ADMIN DASHBOARD ROUTES DOCUMENTATION

## Overview
The admin_dashboard blueprint handles all the admin-related processes for the application, including admin dashboard, for products, users, orders, etc

1. Admin dashboard
**Endpoint: **
`/admin/dashboard`
method: GET

## Description
Admin dasboard retrieves all the content related to the admin based on the user's role as admin.
Authentication: Requires a valid JWT token (@jwt_required)

Responses:
200:
If the user details as an admin are found.

403:
If the user is unauthorized:
```json
{
    "error": "Unathorized access"
}
```

2. View or Add products
URL: `/admin/dashboard/products`
Methods: GET or POST
Authentication: Requires a valid JWT token (@jwt_required)

Responses:
200:
If products are found.
```json
[
    {
    "id": "integer",
    "name": "string",
    "price": "float"
    }
]
```

400:
If the product data provided is invalid.
```json
{
    "error": "Invalid data."
}

201:
For successful product creation
```json
{
    "Message": "Product created successfully",
    "id": "integer",
    "name": "string",
    "price": "float",
    "created_at": "",
    "updated_at": ""
}
```

3. View or Add Services.
URL: `/admin/dashboard/services`
Methods: `GET or POST`
Description: Fetches all services and can add services.
Authentication: Requires a valid JWT token (@jwt_required)

Responses:
200:
If services are found.
```json
[
    {
    "id": "integer",
    "name": "string",
    "price": "float"
    }

    {
    "id": "integer",
    "name": "string",
    "price": "float"
    }
]
```

201:
If the service is created successfully.
```json
{
    "Message": "Service created successfully.",
    "id": "integer",
    "name": "string",
    "price": "float"
}

400:
If the service data is invalid
```json
{
    "error": "Invalid data"
}
```

4. View all Orders.
URL: `/admin/dshboard/orders`
Methods: `GET`
Description: Fetches all the orders them.
Authentication: Requires a valid JWT token (@jwt_required)

Responses:
200:
If the orders are found.
```json
[
    {
    "id": "integer",
    "status": "string",
    "total_amount": "float",
    "order_date": "DateTime"
    }
]
```

400:
If the data for orders is invalid
```json
{
    "error":"Invalid data"
}
```

4. View all users.
URL: `/admin/dashboard/users`

Method: GET
Description: Fetches the all the users' profile details.
Authentication: Requires a valid JWT token (@jwt_required()).

Responses:
200:
If profile details are found.
Example:
```json
{
  "id": "integer",
  "username": "string",
  "email": "string",
  "role": "string"
}
```

404:
If the no users are found.
Example:
```json
{ "error": "Users not found" }
```

5. Update a User
URL: `/admin/dashboard/users/<int:id>`
Method: PUT
Description: Updates the current user's profile details.

Authentication: Requires a valid JWT token (@jwt_required()).

400:
Request Body:
```json
{
  "error": "Role is required"
}
```
Responses:
200:
On successful update.
Example:
```json
{
  "id": "integer",
  "name": "string",
  "email": "string",
  "role": "stirng"
}
```

6. Delete a User
URL: `/admin/dashboard/users/<int:id>`
Method: DELETE
Description: Deletes the user's profile details.
Authentication: Requires a valid JWT token (@jwt_required()).

404:
If the user is not found
Request Body:
```json
{
  "error": "User not found."
}
```
Responses:
200:
On successful delete.
Example:
```json
{
  "message": "User deleted successfully",
}
```

500:
If there is an internal server error or unknown error
```json
{
    "error": "string"
}



