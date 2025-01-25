## Authentication Routes Documentation

## Overview
The auth blueprint handles all authentication-related processes for the application, including user registration, login, password resets, and email verification. These endpoints are secured and use JWT for token-based authentication.

1. Register a New User
**Endpoint:**
`/auth/register/`
method: POST

## Description:
Registers a new user by taking required details and optionally additional fields like first and last name.

**Request Body:**

```json
{
  "username": "string (required)",
  "email": "string (required)",
  "password": "string (required)",
  "firstname": "string (optional)",
  "lastname": "string (optional)"
}
```
Response:

201 Created: User registered successfully.
```json
{
  "message": "User registered successfully",
  "user": { "id": 1, "username": "johndoe", "email": "john@example.com" }
}
```

400 Bad Request: Invalid input or data.
```json
{ "error": "Invalid JSON" }
```
500 Internal Server Error: Unexpected error.


2. Login
**Endpoint:**
`POST /auth/login`

Description:
Authenticates a user by verifying their email and password.

Request Body:

```json
{
  "email": "string (required)",
  "password": "string (required)"
}
```
Response:

200 OK: Login successful, returns access and refresh tokens.
```json
{
  "message": "Login successful",
  "access_token": "string",
  "refresh_token": "string"
}
```

401 Unauthorized: Invalid email or password.
```json
{ "error": "Invalid email or password" }
```
400 Bad Request: Missing or invalid data.
500 Internal Server Error: Unexpected error.


3. Logout
Endpoint:
POST /auth/logout

Description:
Logs out the current user.

Headers:

Authorization: Bearer <access_token>
Response:

200 OK: Logout successful.
```json
{ "message": "Logout successful" }
```

4. Refresh Access Token
Endpoint:
POST /auth/refresh

Description:
Refreshes the user's access token using the refresh token.

Headers:

Authorization: Bearer <refresh_token>
Response:
200 OK: Returns a new access token.
```json
{ "access_token": "string" }
```
401 Unauthorized: Invalid or missing refresh token.


5. Request Password Reset
Endpoint:
POST /auth/request-password-reset

Description:
Sends a password reset email to the user.

Request Body:

```json
{
  "email": "string (required)"
}
```
Response:

200 OK: Reset email sent if the user exists.
```json
{ "message": "Check your email, a password reset email has been sent" }
```
400 Bad Request: Missing email field.


6. Reset Password
Endpoint:
POST /auth/password-reset/<token>

Description:
Resets the user's password using a token.

Request Body:

```json
{
  "password": "string (required)"
}
```
Response:

200 OK: Password reset successful.
```json
{ "message": "Password has been reset successfully." }
```
400 Bad Request: Invalid or expired token, or missing password field.


7. Request Email Verification
Endpoint:
POST /auth/request-verify-email

Description:
Sends a verification email to the user.

Request Body:

```json
{
  "email": "string (required)"
}
```
Response:

200 OK: Verification email sent.
```json
{ "message": "Check your email, a verification link has been sent." }
```
400 Bad Request: Missing email field.


8. Verify Email
Endpoint:
POST /auth/verify-email/<token>

Description:
Verifies a user's email using a token.

Response:

200 OK: Email verified successfully.
```json
{ "message": "Email has been verified successfully." }
```

400 Bad Request: Invalid or expired token.
```json
{ "message": "Invalid or expired token." }
```
