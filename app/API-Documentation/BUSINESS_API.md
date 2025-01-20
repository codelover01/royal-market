## Business API Endpoints
This document provides details about the available endpoints for managing businesses in the application.

# Base URL
All endpoints are prefixed with /business.

1. Create Business
**Endpoint:** `/business/create_business`
**Method:** `POST`
Authorization: JWT token required

# Description:
Adds a new business to the database.

Request Body:

```json
{
  "name": "Business Name",
  "email": "business@example.com",
  "owner_id": 1,
  "description": "A brief description of the business.",
  "location": "City, State",
  "online_available": true,
  "offline_available": false
}```
Responses:

201 Created
json
{
  "message": "Business created successfully",
  "New_business": {
    "id": 1,
    "name": "Business Name",
    "email": "business@example.com",
    "description": "A brief description of the business.",
    "location": "City, State",
    "online_available": true,
    "offline_available": false,
    "owner_id": 1
  }
}
400 Bad Request: Invalid JSON or missing required fields.
404 Not Found: User not found.
500 Internal Server Error: Unexpected error.

2. Update Business
**Endpoint:** `/business/update_business/<business_id>`
**Method:** `PUT`
Authorization: JWT token required

Description:
Updates the credentials of an existing business.

Request Body:
All fields are optional. If a field is not provided, its value will remain unchanged.

json
{
  "name": "Updated Business Name",
  "email": "updated@example.com",
  "description": "Updated description.",
  "location": "New City, State",
  "online_available": false,
  "offline_available": true
}
Responses:

200 OK:
json
{
  "Message": "Business updated successfully."
}
400 Bad Request: Invalid JSON or business not found.
403 Forbidden: User does not own the business.
500 Internal Server Error: Unexpected error.


3. Delete Business
**Endpoint:** `/business/delete_business/<business_id>`
**Method:**  `DELETE`
Authorization: JWT token required

Description:
Deletes a business from the database by its ID.

Responses:

`200 OK:`
json
{
  "message": "Business deleted successfully"
}
403 Forbidden: User does not own the business.
500 Internal Server Error: Unexpected error.
4. Get User's Businesses
Endpoint: /business/get_businessses
Method: GET
Authorization: JWT token required

Description:
Retrieves all businesses associated with the authenticated user.

Responses:

200 OK:
json
[
  {
    "message": "These are your business credentials.",
    "id": 1,
    "name": "Business Name",
    "email": "business@example.com",
    "description": "A brief description.",
    "location": "City, State",
    "online_available": true,
    "offline_available": false,
    "created_at": "2023-01-01T12:00:00",
    "updated_at": "2023-01-02T12:00:00"
  }
]
404 Not Found: No businesses found for the user's account.
500 Internal Server Error: Unexpected error.