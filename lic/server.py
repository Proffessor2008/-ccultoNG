import json
import secrets
import smtplib
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import stripe
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configuration
stripe.api_key = 'your-stripe-secret-key'
SMTP_SERVER = 'https://occulto.pro'
SMTP_PORT = 587
SENDER_EMAIL = 'tudubambam@ya.ru'
SENDER_PASSWORD = '12345'

# License pricing
PRICING = {
    'developer': 99,
    'professional': 499,
    'enterprise': 'custom'
}


# Generate license key
def generate_license_key():
    """Generate a unique license key"""
    return f"OCCULTO-{secrets.token_hex(16).upper()}"


# Send email
def send_email(to_email, subject, body):
    """Send email with license information"""
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False


# API: Process payment
@app.route('/api/purchase', methods=['POST'])
def purchase_license():
    """Process license purchase"""
    data = request.json
    email = data.get('email')
    name = data.get('name')
    tier = data.get('tier')

    if not all([email, name, tier]):
        return jsonify({'error': 'Missing fields'}), 400

    if tier not in PRICING:
        return jsonify({'error': 'Invalid tier'}), 400

    try:
        # Generate license
        license_key = generate_license_key()
        expiry_date = (datetime.now() + timedelta(days=365)).isoformat()

        # Prepare license data
        license_data = {
            'key': license_key,
            'tier': tier,
            'buyer': name,
            'purchase_date': datetime.now().isoformat(),
            'expiry_date': expiry_date,
            'status': 'active'
        }

        # Save to database
        save_license(license_data)

        # Send email
        email_body = f"""
        <h2>ØccultoNG Pro License</h2>
        <p>Спасибо за покупку!</p>
        <p><strong>Лицензионный ключ:</strong> {license_key}</p>
        <p><strong>План:</strong> {tier.capitalize()}</p>
        <p><strong>Действительна до:</strong> {expiry_date}</p>
        <p>Поместите лицензионный файл в ~/.occulto_ng/license.json</p>
        <p>Спасибо за использование ØccultoNG Pro!</p>
        """

        send_email(email, 'ØccultoNG Pro License', email_body)

        return jsonify({
            'success': True,
            'license_key': license_key,
            'expiry_date': expiry_date
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# API: Enterprise contact
@app.route('/api/contact-enterprise', methods=['POST'])
def contact_enterprise():
    """Handle enterprise license inquiry"""
    data = request.json
    company = data.get('company')
    email = data.get('email')
    phone = data.get('phone')
    message = data.get('message')

    # Send to admin email
    admin_message = f"""
    <h2>Enterprise License Inquiry</h2>
    <p><strong>Company:</strong> {company}</p>
    <p><strong>Email:</strong> {email}</p>
    <p><strong>Phone:</strong> {phone}</p>
    <p><strong>Message:</strong> {message}</p>
    """

    send_email('sales@occulto-ng.com', 'Enterprise License Inquiry', admin_message)

    return jsonify({'success': True})


# API: Academic license
@app.route('/api/academic-license', methods=['POST'])
def academic_license():
    """Handle academic license request"""
    data = request.json
    email = data.get('email')

    if not email.endswith('.edu'):
        return jsonify({'error': 'Not a university email'}), 400

    # Generate academic license
    license_key = generate_license_key()

    email_body = f"""
    <h2>ØccultoNG Pro Academic License</h2>
    <p>Спасибо за применение на Academic License!</p>
    <p><strong>Лицензионный ключ:</strong> {license_key}</p>
    <p>Этот ключ действует неограниченно для образовательных целей.</p>
    <p>Пожалуйста, указывайте авторство в публикациях.</p>
    """

    send_email(email, 'ØccultoNG Pro Academic License', email_body)

    return jsonify({'success': True})


# Database functions
def save_license(license_data):
    """Save license to database"""
    # In production, use a real database (PostgreSQL, MongoDB, etc.)
    with open('licenses.json', 'a') as f:
        f.write(json.dumps(license_data) + '\n')


def load_licenses():
    """Load licenses from database"""
    try:
        with open('licenses.json', 'r') as f:
            return [json.loads(line) for line in f]
    except:
        return []


if __name__ == '__main__':
    app.run(debug=True, port=5000)
