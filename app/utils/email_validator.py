from email_validator import validate_email, EmailNotValidError

# Utility function to validate email
def is_valid_email(email: str) -> bool:
    """An endpoint to valid an email's format"""
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False
