
from models.users import User

import smtplib
from flask import Blueprint, current_app as app, url_for


email_bp = Blueprint('email_bp', __name__, url_prefix='/email')

@email_bp.route('/send-test-email', methods=['GET', 'POST'])
def send_test_email():
    try:
        # Set up the SMTP server connection
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.set_debuglevel(1)  # Enable debug output for SMTP connection
        smtp.ehlo()  # Send EHLO to the server to initiate the communication
        smtp.starttls()  # Secure the connection using TLS
        smtp.login('royalmarketv1@gmail.com', 'dpqg aqlz pmdf prce')
        
        # Create the email message
        from_email = 'royalmarketv1@gmail.com'  # Sender's email address
        to_email = 'kinglovenoel@gmail.com'  # Recipient's email address
        subject = "Test Email from Royal Market"
        body = "This is a test email sent from the Royal Market app."
        
        # Construct the email message
        message = f"Subject: {subject}\n\n{body}"
        
        # Send the email
        smtp.sendmail(from_email, to_email, message)
        smtp.quit()  # Close the SMTP connection
        
        return "Test email sent successfully!"
    
    except Exception as e:
        return f"Error sending email: {e}"

def send_password_reset_email(user: User):
    """
    Sends a password reset email to the user using smtplib.
    """
    try:
        token = user.password_reset_token()
        msg = f"Subject: Password Reset Request\n\nTo reset your password, visit the following link:\n" \
              f"{url_for('auth.request_password_reset', token=token, _external=True)}\n" \
              f"If you did not make this request, simply ignore this email."
        
        # Set up the SMTP server connection
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.set_debuglevel(1)
        smtp.ehlo()
        smtp.starttls()
        smtp.login('royalmarketv1@gmail.com', 'dpqg aqlz pmdf prce')
        
        # Send the email
        smtp.sendmail('royalmarketv1@gmail.com', user.email, msg)
        smtp.quit()
    except Exception as e:
        return f"Error sending email: {e}"

def send_verification_email(user: User):
    """ Sends an email that verifies the validity of the user's email using smtplib. """
    try:
        token = user.email_verification_token()
        msg = f"Subject: Verify Your Email\n\nPlease verify your email by clicking on the following link:\n" \
              f"{url_for('auth.verify_email', token=token, _external=True)}"
        
        # Set up the SMTP server connection
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.set_debuglevel(1)
        smtp.ehlo()
        smtp.starttls()
        smtp.login('royalmarketv1@gmail.com', 'dpqg aqlz pmdf prce')

        
        # Send the email
        smtp.sendmail('royalmarketv1@gmail.com', user.email, msg)
        smtp.quit()
    except Exception as e:
        return f"Error sending email: {e}"
