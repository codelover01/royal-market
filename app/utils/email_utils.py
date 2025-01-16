
from models.users import User
import smtplib
from flask import url_for



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
