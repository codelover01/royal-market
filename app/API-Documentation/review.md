## Review API Documentation

# Base url
/review

1. Create Review
URL: /review/create-reviews
Method: POST
Description: Allows authenticated users to create a new review for a product or service. The review includes a comment and a rating between 1 and 5.

Request Body:
```json
{
  "comment": "string",  // The review comment
  "rating": "integer",  // The rating (1-5)
  "product_id": "integer",  // (Optional) The ID of the product being reviewed
  "service_id": "integer"  // (Optional) The ID of the service being reviewed
}
```
Responses:
201:
Review created successfully.
Example:
```json
{
  "id": "integer",
  "comment": "string",
  "rating": "integer",
  "created_at": "string"
}
```

400:
If required fields are missing or the rating is invalid.
```json
{ "message": "Missing required fields: comment and rating" }
```


2. Get Reviews
URL: /review/get-reviews/<review_type>/<item_id>
Method: GET
Description: Retrieves reviews for a specific product or service.
URL Parameters:
review_type: The type of the item ('product' or 'service').
item_id: The ID of the product or service.

Responses:
200:
If reviews are found.
```json
{
  "reviews": [
    {
      "id": "integer",
      "user": "string",  // The username of the reviewer
      "comment": "string",
      "rating": "integer",
      "review_date": "string"
    }
  ]
}
```

400:
If the review type is invalid.
Example:
```json
{ "message": "Invalid review type. Use 'product' or 'service'." }
```

404:
If no reviews are found.
```json
{ "message": "No reviews found for this product/service." }
```

3. Update Review
URL: /review/update-reviews/<review_id>
Method: PUT
Description: Allows authenticated users to update their own reviews. Only the comment and rating fields can be updated.
URL Parameters:
review_id: The ID of the review to be updated.
Request Body:
```json
{
  "comment": "string",  // The updated review comment
  "rating": "integer"  // The updated rating (1-5)
}
```

Responses:
200:
If the review is updated successfully.
```json
{
  "id": "integer",
  "comment": "string",
  "rating": "integer",
  "created_at": "string"
}
```

400:
If the rating is invalid.
```json
{ "message": "Invalid rating" }
```

403:
If the user is not authorized to update the review.
```json
{ "message": "You can only edit your own reviews." }
```

4. Delete Review
URL: /review/delete-reviews/<review_id>
Method: DELETE
Description: Allows authenticated users to delete their own reviews.
URL Parameters:
review_id: The ID of the review to be deleted.

Responses:
200:
If the review is deleted successfully.
```json
{ "message": "Review deleted successfully." }
```

403:
If the user is not authorized to delete the review.
```json
{ "message": "You can only delete your own reviews." }
```