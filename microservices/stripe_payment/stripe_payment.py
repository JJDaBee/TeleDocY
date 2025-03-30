# app.py
from flask import Flask, request, jsonify, redirect
import stripe
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# Set Stripe API key from environment (fallback to empty string if missing)
stripe.api_key = os.getenv('STRIPE_SECRET_KEY', '')
PORT = int(os.environ.get('PORT', 3001))

@app.route('/create-checkout', methods=['POST'])
def create_checkout():
    try:
        data = request.json
        amount = data.get('amount')
        description = data.get('description', 'Payment')
        
        # Create a Checkout Session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            mode='payment',
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': description,
                    },
                    'unit_amount': amount,  # Amount in cents
                },
                'quantity': 1,
            }],
            success_url=f"http://localhost:{PORT}/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"http://localhost:{PORT}/cancel",
        )
        
        # Return just the checkout URL
        return jsonify({'url': session.url})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/success')
def success():
    return 'Payment successful!'

@app.route('/cancel')
def cancel():
    return 'Payment canceled.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True)