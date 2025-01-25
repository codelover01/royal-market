## PAYMENT API DOCUMENTATION

# Base url
/payments

1. Create Payment
URL: /payments/create
Method: POST
Description: Creates a new payment for an order.
Request Body:
```json
{
  "order_id": "integer",  // The ID of the order
  "payment_method": "string",  // Payment method (e.g., Credit Card, PayPal)
  "payment_amount": "integer"  // The amount to be paid
}
```

Responses:
400:
If the request body is invalid or required fields are missing.
Example:
```json
{ "message": "Invalid JSON data" }
```

200:
On successful payment creation.
Example:
```json
{ "Payment successful.": "result" }
```

2. Get Payment by ID
URL: /payments/<payment_id>
Method: GET
Description: Retrieves the details of a payment by its ID.
URL Parameters:
payment_id: The ID of the payment.

Responses:
200:
If payment is found.
Example:
```json
{
  "id": "integer",
  "order_id": "integer",
  "payment_date": "string",
  "payment_method": "string",
  "payment_amount": "integer",
  "payment_status": "string"
}
```

404:
If the payment ID is not found.
Example:
```json
{ "Payment details.": "result" }
```

3. Get All Payments
URL: /payments/
Method: GET
Description: Retrieves all payments.
Responses:
200:
If payments are found.
Example:
```json
{
  "Payments found": [
    {
      "id": "integer",
      "order_id": "integer",
      "payment_date": "string",
      "payment_method": "string",
      "payment_amount": "integer",
      "payment_status": "string"
    }
  ]
}
```

404:
If no payments are found.
Example:
```json
{ "error": "No payments were found" }
```

500:
For internal server errors.
```json
{ "error": "Error message" }
```

4. Refund Payment
URL: /payments/refund/<payment_id>
Method: POST
Description: Processes a refund for a payment.
URL Parameters:
payment_id: The ID of the payment to be refunded.

Responses:
200:
If the refund is successful.
```json
{ "Successful payment refund.": "result" }
```

400:
If the payment ID is invalid or missing.
```json
{ "error": "Payment ID missing or Invalid" }
```