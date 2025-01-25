## Services API Documentation
# Base URL
All endpoints are prefixed with /services

1. Add a New Service
**Endpoint:**
`POST /services/add_services`

Description:
Adds a new service to a business owned by the current user.

Request Headers:

Content-Type: application/json
Authorization: Bearer <JWT_TOKEN> (if using token-based authentication)
Request Body:

```json
{
  "business_id": 1,
  "name": "Haircut",
  "description": "A professional haircut service.",
  "hourly_cost": 20,
  "duration": 30
}
```
Response:
Success (201):

```json
{
  "message": "Service added successfully",
  "service": {
    "id": 101,
    "name": "Haircut",
    "description": "A professional haircut service.",
    "hourly_cost": 20,
    "duration": 30,
    "business_id": 1
  }
}
```

Error (400): Invalid JSON or missing fields.
```json
{
  "error": "Invalid JSON"
}
```

Error (403): Unauthorized or invalid business ownership.
```json
{
  "error": "Invalid business ID or unauthorized access."
}
```

Error (500): Internal server error.
```json
{
  "error": "Database error message here"
}
```

2. List All Services
Endpoint:
GET /services/list_services

Description:
Lists all services available in the system.

Request Headers:

Authorization: Bearer <JWT_TOKEN> (if required)
Request Parameters:
None

Response:
Success (200):
```json
{
  "services": [
    {
      "id": 101,
      "name": "Haircut",
      "description": "A professional haircut service.",
      "hourly_cost": 20,
      "duration": 30,
      "business_id": 1
    },
    {
      "id": 102,
      "name": "Massage",
      "description": "A relaxing massage service.",
      "hourly_cost": 50,
      "duration": 60,
      "business_id": 2
    }
  ]
}
```

Error (500): Internal server error.
```json
{
  "error": "Database error message here"
}
```

3. Delete a Service
Endpoint:
DELETE /services/delete_services/<service_id>

Description:
Deletes a service by its unique ID, ensuring the current user owns the business it belongs to.

Request Headers:
Authorization: Bearer <JWT_TOKEN> (if required)
Path Parameters:

service_id (integer): The ID of the service to delete.
Response:

Success (200):
```json
{
  "message": "Service deleted successfully"
}
```

Error (403): Unauthorized access to the service.
```json
{
  "error": "Unauthorized: You don't own this service."
}
```

Error (404): Service not found.
```json
{
  "error": "Service with ID <service_id> not found."
}
```

Error (500): Internal server error.
```json
{
  "error": "Database error message here"
}
```

Common Errors
401: Unauthorized
Occurs when the user is not authenticated.
```json
{
  "error": "Unauthorized access. Please log in."
}
```

500: Internal Server Error
Occurs when there's an unhandled exception in the server.
```json
{
  "error": "An unexpected error occurred. Please try again later."
}
```