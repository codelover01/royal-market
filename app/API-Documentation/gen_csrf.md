## CSRF Token API Documentation

## Overview
This module is responsible for generating and handling CSRF tokens to secure requests against Cross-Site Request Forgery (CSRF) attacks. It provides routes for generating tokens, verifies tokens in requests, and applies additional security measures like Content Security Policy (CSP).

# Base URL
All endpoints are prefixed with /gen_csrf

Endpoints
1. Generate CSRF Token
**Endpoint:**
`GET /gen_csrf/csrf-token`

Description:
Generates a CSRF token and sets it in a secure cookie with the SameSite attribute. The token can also be retrieved in the response body for use in frontend requests.

Request Headers:
None required.

Request Parameters:
None.

Response:

Success (200):
The CSRF token is returned in the response body and also set in a cookie named csrf_token.

```json
{
  "csrf_token": "<generated_csrf_token>"
}
```
Cookie:

csrf_token: The CSRF token is set with attributes:
SameSite=Lax
HttpOnly=False
Secure=False (Use True in production with HTTPS)
Error:
This endpoint does not return errors under normal circumstances.


2. CSRF Protection Middleware

# Description:
Verifies the CSRF token provided in cookies and headers for POST, PUT, and DELETE requests.

Request Headers:

X-CSRFToken: The CSRF token sent by the client (e.g., frontend) in headers.
Request Cookies:

csrf_token: The CSRF token stored in the browser's cookies.
Validation:

Both the csrf_token cookie and the X-CSRFToken header must be present.
The tokens in the cookie and header must match.
Response:

Success: Proceeds with the request if validation is successful.
Error (400):
If either token is missing:
```json
{
  "error": "CSRF token missing"
}
```

If the tokens do not match:
```json
{
  "error": "CSRF token mismatch"
}
```


3. Content Security Policy (CSP)
Description:
Applies a Content Security Policy (CSP) to all responses to mitigate XSS attacks by blocking external scripts and unsafe object execution.

CSP Header:
http
Content-Security-Policy: script-src 'self' 'strict-dynamic'; object-src 'none';
Response Impact:
All responses include the CSP header. No changes are made to the body.

4. Log CSRF Tokens
Description:
Logs the CSRF tokens received in headers and cookies after every request for debugging purposes.

Log Output:
plaintext
Request CSRF Token: <header_csrf_token>
Cookie CSRF Token: <cookie_csrf_token>

# Common Errors
`400`: CSRF Token Missing
Occurs when either the csrf_token cookie or the X-CSRFToken header is not provided in the request.

`400`: CSRF Token Mismatch
Occurs when the csrf_token cookie value does not match the X-CSRFToken header value.

# Security Considerations
Secure Cookie: Use secure=True for the csrf_token cookie in production to ensure it is only transmitted over HTTPS.
CSP: The strong CSP applied reduces the risk of XSS attacks by restricting external scripts.
Logging: Avoid logging sensitive token data in production environments.
