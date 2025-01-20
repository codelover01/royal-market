# royal-market

# 🛒 Royal Market Backend
Welcome to the Royal Market Backend Repository! This project powers the core functionalities of Royal Market, providing robust backend services for managing businesses, products, services, and notifications.

📚 Table of Contents
# Overview
# Technologies Used
# Project Architecture
# Setup Instructions
# Usage Guidelines
# API Documentation
# Contributing
# License


# 🚀 1. Overview
Royal Market is a platform that allows businesses to:

Manage products and services efficiently.
Send notifications and updates to users.
Streamline backend workflows for admins and business owners.
This backend system handles user authentication, product management, notifications, and business profiles with a scalable architecture.

# 🛠️ 2. Technologies Used
Programming Language: Python
Web Framework: Flask
Database: MySQL
ORM: SQLAlchemy
Authentication: Flask-jwt-extended, Flask-Bcrypt
Security: CSRF Protection via Flask-WTF
Deployment: Render for application and Railway for database

# 🏗️ 3. Project Architecture
High-Level Diagram:
(A diagram showing flow between backend, and database.)

# Key Components:
Models: Define database schemas (e.g., Business, Product, Service).
Services: Business logic encapsulated in classes (e.g., BusinessService, ProductService).
Routes: RESTful API endpoints.
Authentication: Secure user login/logout system.

# 🧩 4. Setup Instructions
Prerequisites:
Ensure you have the following installed:

Python 3.10+
MySQL 8.4+
pip (Python package manager)

Step 1: Clone the Repository
git clone https://github.com/coderlover01/royal-market.git
cd royal-market

Step 2: Install Dependencies
pip install -r requirements.txt

Step 3: Configure Environment Variables
Create a .env file in the root directory:

Step 4: Initialize the Database
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

Step 5: Run the Application
Access the application at: [https://royal-market.onrender.com]

# 📝 5. Usage Guidelines
Running in Development Mode:
flask run --debug
Accessing the Admin Dashboard:
Visit: [https://royal-market.onrender.com/admin]

Testing API Endpoints:
Use Postman to test the endpoints.
Ensure the database is seeded with sample data.

Example API Call:

# Get all products:
GET /api/products

# Add a new product:
POST /api/products
Content-Type: application/json

{
  "name": "Product Name",
  "price": 50.0,
  "stock": 100
}

# 📑 6. API Documentation ONE
Explore endpoints for products, businesses, notifications, and authentication
app/API-Document

## Authentication API Routes Documentation

## Overview
The auth blueprint handles all authentication-related processes for the application, including user registration, login, password resets, and email verification. These endpoints are secured and use JWT for token-based authentication.

1. Register a New User
**Endpoint:**
`POST /auth/register/`

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
``json
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
json
{ "message": "Logout successful" }


4. Refresh Access Token
Endpoint:
POST /auth/refresh

Description:
Refreshes the user's access token using the refresh token.

Headers:

Authorization: Bearer <refresh_token>
Response:
200 OK: Returns a new access token.
json
{ "access_token": "string" }

401 Unauthorized: Invalid or missing refresh token.


5. Request Password Reset
Endpoint:
POST /auth/request-password-reset

Description:
Sends a password reset email to the user.

Request Body:

json
{
  "email": "string (required)"
}
Response:

200 OK: Reset email sent if the user exists.
json
{ "message": "Check your email, a password reset email has been sent" }
400 Bad Request: Missing email field.


6. Reset Password
Endpoint:
POST /auth/password-reset/<token>

Description:
Resets the user's password using a token.

Request Body:

json
{
  "password": "string (required)"
}
Response:

200 OK: Password reset successful.
json
{ "message": "Password has been reset successfully." }
400 Bad Request: Invalid or expired token, or missing password field.


7. Request Email Verification
Endpoint:
POST /auth/request-verify-email

Description:
Sends a verification email to the user.

Request Body:

json
{
  "email": "string (required)"
}
Response:

200 OK: Verification email sent.
json
{ "message": "Check your email, a verification link has been sent." }
400 Bad Request: Missing email field.


8. Verify Email
Endpoint:
POST /auth/verify-email/<token>

Description:
Verifies a user's email using a token.

Response:

200 OK: Email verified successfully.
json
{ "message": "Email has been verified successfully." }

400 Bad Request: Invalid or expired token.
json
{ "message": "Invalid or expired token." }
```


# 🤝 7. Contributing
We welcome contributions!

How to Contribute:

Fork the repository.
Create a new branch: git checkout -b feature/your-feature.
Make your changes and commit: git commit -m "Add new feature".
Push to your branch: git push origin feature/your-feature.
Open a Pull Request.
Code of Conduct:
Please follow our Code of Conduct.

# 📜 8. License
This project is licensed under the MIT License.

See the full license details in LICENSE.

📞 Contact Information:
Project Lead: Ogwel Noel
GitHub: [https://github.com/codelover01/royal-market]
Email: [kinglovenoel@gmail.com]