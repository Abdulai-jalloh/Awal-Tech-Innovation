from datetime import date
from flask import Blueprint, render_template, request, jsonify, flash
import os, smtplib
from database.message import Message
from dotenv import load_dotenv
load_dotenv()
from database.db import db
from twilio.rest import Client
from email.message import EmailMessage

contact_bp = Blueprint('contact', __name__)

# Load environment variables
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_number = os.getenv('TWILIO_PHONE_NUMBER') 
admin_number = os.getenv('ADMIN_PHONE_NUMBER')
whatsapp_from = os.getenv('TWILIO_WHATSAPP_NUMBER')
whatsapp_to = os.getenv('ADMIN_WHATSAPP_NUMBER')
email_user = os.getenv('EMAIL_USER')
email_password = os.getenv('EMAIL_PASSWORD')
receiver_email = os.getenv('RECEIVER_EMAIL')

client = Client(account_sid, auth_token)

@contact_bp.route('/contact', methods=['GET'])
def contact_page():
    return render_template('contact.html')
    

@contact_bp.route('/contact', methods=['POST'])
def send_phone_contact():
    data = request.get_json()
    if request.method == 'POST':
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        message = data.get('message')

    # Store the message in to the Database
    new_message = Message(name=name, email=email, phone=phone, message=message, subject="Contact Form Submission")
    db.session.add(new_message)
    db.session.commit()
    print('message stored in db', new_message)
    full_message = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}"
    success = False
    print('message prepared', full_message)
    # Try SMS
    try:
        client.messages.create(body=full_message, from_=twilio_number, to=admin_number)
        success = True
    except Exception as e:
        print(f"SMS Error: {e}")

    # Try WhatsApp (optional)
    try:
        client.messages.create(body=full_message, from_=whatsapp_from, to=whatsapp_to)
        success = True
    except Exception as e:
        print(f"WhatsApp Error: {e}")
    
    if success:
        print('message sent successfully')
        return jsonify({'success': True, 'message': 'Thank you for contacting Awal Tech Innovations We will reach back to you as soon as possible'}), 200
    else:
        return jsonify({'success': False, 'message': 'Failed to send message.'}), 500
    

@contact_bp.route('/admin/messages', methods=['GET'])
def view_messages():
    messages = Message.query.order_by(Message.timestamp.desc()).all()
    return render_template('admin_messages.html', messages=messages)  

@contact_bp.route('/admin/reply_message/<int:id>', methods=['GET','POST'])
def reply_message(id):
    messages = Message.query.get(id)
    if request.method == 'POST':
        reply_content = request.form.get('reply')
        try:
            msg = EmailMessage()
            msg.set_content(reply_content)
            msg['Subject'] = 'Reply to your message'
            msg['From'] = email_user
            msg['To'] = messages.email

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(email_user, email_password)
                smtp.send_message(msg)
            flash('Reply sent successfully!', 'success')
        except Exception as e:
            flash(f'Failed to send reply: {e}', 'danger')
    return render_template('reply_message.html', messages=messages)