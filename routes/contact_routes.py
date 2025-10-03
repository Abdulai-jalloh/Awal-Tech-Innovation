from flask import  request, redirect, url_for, flash, render_template, Blueprint
import os
from twilio.rest import Client
from email.message import EmailMessage
import smtplib

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auto_taken = os.getenv('TWILIO_AUTH_TOKEN')
Twilio_number = os.getenv('TWILIO_PHONE_NUMBER')
Admin_number = os.getenv('ADMIN_PHONE_NUMBER')

#whatsapp
twil_whatsapp_num = os.getenv('TWILIO_WHATSAPP_NUMBER')
Admin_whatsapp_num = os.getenv('ADMIN_WHATSAPP_NUMBER')

#Email
email_user = os.getenv('EMAIL_USER')
email_password = os.getenv('EMAIL_PASSWORD')
reciver_email = os.getenv('RECEIVER_EMAIL')

client = Client(account_sid, auto_taken)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

contact_bp = Blueprint('contacts', __name__)

@contact_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        full_infoMessage = (
            f"Message from: {name} {email}\n"
            f"Message: {message}"
        )
        success = False
        # Try SMS
        try:
            client.messages.create(
                body=full_infoMessage,
                from_=Twilio_number,
                to=Admin_number
            )
            success = True
        except Exception as e:
            print(f"SMS error: {e}")

        # Try WhatsApp
        try:
            client.messages.create(
                body=full_infoMessage,
                from_=twil_whatsapp_num,
                to=Admin_whatsapp_num
            )
            success = True
        except Exception as e:
            print(f"WhatsApp error: {e}")

        # Try Email
        try:
            msg = EmailMessage()
            msg.set_content(full_infoMessage)
            msg['Subject'] = 'Clients'
            msg['From'] = email_user
            msg['To'] = reciver_email

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(email_user, email_password)
                smtp.send_message(msg)
            success = True
        except Exception as e:
            print(f"Email error: {e}")

        if success:
            flash('Thank you for contacting us! We will reach back to you as soon as possible.', 'success')
          # Optionally, you can also send a confirmation email to the user here

        else:
            flash('Something went wrong while sending your message. Please try again.', 'danger')
        return redirect(url_for('contact.contact'))
    
    return render_template('contact.html')