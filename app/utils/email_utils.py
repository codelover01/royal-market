# import sys
# import os

# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from flask_mail import Message, Mail
# from flask import url_for
from models.users import User

# mail = Mail()


# def send_password_reset_email(user: User):
#     """
#     Sends a password reset email to the user.
#     """
#     #from app import mail
#     token = user.password_reset_token()
#     msg = Message('Password Reset Request', recipients = [user.email])
#     msg.body = (f'''To reset your password, visit the following link:
# {url_for('email_bp.request_password_reset', token=token, _external=True)}
# If you did not make this request, simply ignore this email.
# ''')
    
#     mail.send(msg)

# def send_verification_email(user: User):
#     """ Sends an email that verifies the validity of the
#     user's email.
#     """
#     #from app.app import mail
#     token = user.email_verification_token()
#     msg = Message('Verify Your Email', recipients=[user.email])
#     msg.body = f'''Please verify your email by clicking on the following link:
# {url_for('email_bp.verify_email', token=token, _external=True)}
# '''
#     mail.send(msg)


import sys
import os
import smtplib
from flask import Blueprint, current_app as app, url_for

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Define Blueprint for email_bpentication (or use the existing one)
email_bp = Blueprint('email_bp', __name__)

@email_bp.route('/send-test-email', methods=['GET', 'POST'])
def send_test_email():
    try:
        # Set up the SMTP server connection
        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.set_debuglevel(1)  # Enable debug output for SMTP connection
        smtp.ehlo()  # Send EHLO to the server to initiate the communication
        smtp.starttls()  # Secure the connection using TLS
        smtp.login('royalmarketv1@gmail.com', 'dpqg aqlz pmdf prce')  # Login with the email and password (replace with your credentials)
        
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
