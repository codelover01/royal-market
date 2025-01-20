## User Dashboard API Documentation

## Base URL
/user

1. User Dashboard Overview
URL: /user/dashboard
Method: GET
Description: Retrieves the user's dashboard overview, including basic user details.
Authentication: Requires a valid JWT token (@jwt_required()).

Responses:
200:
If the user details are found.
Example:
```json
{
  "id": "integer",
  "name": "string",
  "email": "string"
}

404:
If the user is not found.
Example:
json
{ "error": "User not found" }


2. User Orders
URL: /user/dashboard/orders
Method: GET
Description: Fetches all orders made by the user.
Authentication: Requires a valid JWT token (@jwt_required()).

Responses:
200:
If orders are found.
Example:
json
[
  {
    "id": "integer",
    "product_name": "string",
    "quantity": "integer",
    "status": "string",
    "order_date": "YYYY-MM-DD"
  }
]

500:
If there is an error fetching the orders.
Example:
json
{ "error": "Error message" }


3. User Cart
URL: /user/dashboard/cart
Method: GET
Description: Fetches the items currently in the user's shopping cart.
Authentication: Requires a valid JWT token (@jwt_required()).

Responses:
200:
If cart items are found.
Example:
json
[
  {
    "id": "integer",
    "product_name": "string",
    "quantity": "integer",
    "price": "integer",
    "status": "string"
  }
]

500:
If there is an error fetching the cart details.
Example:
json
{ "error": "Error message" }


4. User Profile
URL: /user/dashboard/profile

Method: GET

Description: Fetches the current user's profile details.

Authentication: Requires a valid JWT token (@jwt_required()).

Responses:

200:
If profile details are found.
Example:
json
{
  "id": "integer",
  "name": "string",
  "email": "string"
}

404:
If the user profile is not found.
Example:
json
{ "error": "User not found" }
Method: PUT

Description: Updates the current user's profile details.

Authentication: Requires a valid JWT token (@jwt_required()).

Request Body:

json
{
  "name": "string",
  "email": "string"
}
Responses:

200:
On successful update.
Example:
json
{
  "id": "integer",
  "name": "string",
  "email": "string"
}

404:
If the user is not found.
Example:
json
{ "error": "User not found" }


5. Update User
URL: /user/update
Method: PUT
Description: Updates the user's username, email, and password.
Authentication: Requires a valid JWT token (@jwt_required()).
Request Body:
json
{
  "username": "string",
  "email": "string",
  "password": "string"
}

Responses:
200:
On successful update.
Example:
json
{
  "message": "User updated successfully.",
  "user": {
    "id": "integer",
    "username": "string",
    "email": "string"
  }
}

400:
If there is an error in the update request.
Example:
json
{ "error": "Invalid input data" }


6. Delete User
URL: /user/delete
Method: DELETE
Description: Deletes the user's account.
Authentication: Requires a valid JWT token (@jwt_required()).

Responses:
200:
On successful account deletion.
Example:
json
{ "message": "User account deleted successfully" }

400:
If there is an issue deleting the user.
Example:
json
{ "error": "User not found" }