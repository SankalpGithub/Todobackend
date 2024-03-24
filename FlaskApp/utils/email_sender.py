import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def email_sender(email, otp):
    # Sender's email credentials
    sender_email = "22co17@aiktc.ac.in"
    sender_password = "22co17@aiktc"

    # Recipient's email address
    recipient_email = email

    # Create a multipart message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = "OTP for verification"

    # Add body to email
    body = f"OTP - {otp}"
    message.attach(MIMEText(body, "plain"))

    # Create SMTP session
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = message.as_string()
        # Send email
        server.sendmail(sender_email, recipient_email, text)
        return True
    except Exception as e:
        return False
    finally:
        # Close the SMTP server connection
        server.quit()