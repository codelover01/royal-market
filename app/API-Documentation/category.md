## Category Management API Documentation

## Overview
This module is responsible for managing categories, including creating, updating, deleting, and fetching categories and related business, products, and services.

## Base URL
/categories

Endpoints
1. Create Category
Endpoint:
POST /categories/create

Description:
Creates a new category with a specified name and description.

Request Body:

```json
{
    "name": "Category Name",
    "description": "Category Description"
}
Request Headers:

Authorization: Bearer JWT token (for authenticated users).
Response:

Success (201):

json
{
    "message": "Category successfully created.",
    "id": <category_id>,
    "name": "Category Name"
}
Error (400): Invalid JSON data

json
{
    "message": "Invalid JSON data."
}

Error (400): Other related errors
json
{
    "error": "Error message"
}


2. Get All Categories
Endpoint:
GET /categories/

Description:
Fetches all the available categories.

Response:

Success (200):
json
[
    {"id": <category_id>, "name": "Category Name"},
    {"id": <category_id>, "name": "Category Name"}
]


3. Get Category by ID
Endpoint:
GET /categories/<category_id>

Description:
Fetches a specific category by its ID.

Parameters:

category_id: The ID of the category to retrieve.
Response:

Success (200):
json
{
    "id": <category_id>,
    "name": "Category Name",
    "description": "Category Description"
}

Error (404): Category not found
json
{
    "error": "Category not found"
}


4. Update Category
Endpoint:
PUT /categories/<category_id>

Description:
Updates the details of a specific category identified by its ID.

Parameters:

category_id: The ID of the category to update.
Request Body:
json
{
    "name": "Updated Category Name",
    "description": "Updated Category Description"
}
Request Headers:

Authorization: Bearer JWT token (for authenticated users).
Response:

Success (200):
json
{
    "id": <category_id>,
    "name": "Updated Category Name",
    "description": "Updated Category Description"
}

Error (400): Invalid JSON or no data provided
json
{
    "error": "No data provided or Invalid JSON data"
}

Error (404): Category not found
json
{
    "error": "Category not found"
}

Error (400): Other related errors
json
{
    "error": "Error message"
}


5. Delete Category
Endpoint:
DELETE /categories/<category_id>

Description:
Deletes a specific category identified by its ID.

Parameters:

category_id: The ID of the category to delete.
Request Headers:

Authorization: Bearer JWT token (for authenticated users).
Response:

Success (200):
json
{
    "message": "Category deleted successfully."
}

Error (404): Category not found
json
{
    "error": "Category not found"
}


6. List Products under a Category
Endpoint:
GET /categories/<category_id>/products

Description:
Fetches all products under a specific category identified by its ID.

Parameters:

category_id: The ID of the category to fetch products for.
Response:

Success (200):
json
[
    {"id": <product_id>, "name": "Product Name"},
    {"id": <product_id>, "name": "Product Name"}
]

Error (404): Category or products not found
json
{
    "error": "Category or products not found"
}


7. List Services under a Category
Endpoint:
GET /categories/<category_id>/services

Description:
Fetches all services under a specific category identified by its ID.

Parameters:

category_id: The ID of the category to fetch services for.
Response:

Success (200):
json
[
    {"id": <service_id>, "name": "Service Name"},
    {"id": <service_id>, "name": "Service Name"}
]

Error (404): Category or services not found
json
{
    "error": "Category or services not found"
}


8. List Businesses under a Category
Endpoint:
GET /categories/<category_id>/businesses

Description:
Fetches all businesses under a specific category identified by its ID.

Parameters:

category_id: The ID of the category to fetch businesses for.
Response:

Success (200):
json
[
    {"id": <business_id>, "name": "Business Name"},
    {"id": <business_id>, "name": "Business Name"}
]

Error (404): Category or businesses not found
json
{
    "error": "Category or businesses not found"
}

Authentication
Some endpoints require authentication through JWT tokens. The Authorization header must include the Bearer token for endpoints like POST /categories/create, PUT /categories/<category_id>, and DELETE /categories/<category_id>.

Example Header:
http
Authorization: Bearer <your_jwt_token>

Common Errors
400: Invalid Request
Occurs when the request body or parameters are invalid, such as missing or incorrect JSON data.

404: Not Found
Occurs when the specified category, product, service, or business cannot be found.

401: Unauthorized
Occurs when the user does not provide a valid JWT token for authentication.