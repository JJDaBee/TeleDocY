# app.py
from flask import Flask, request, jsonify, redirect
import stripe
import os
import webbrowser
import threading
import time

app = Flask(__name__)

# Set your Stripe API key
stripe.api_key = os.getenv('STRIPE_SECRET_KEY', '')
PORT = 3001

# Store the latest checkout URL for the redirect endpoint
latest_checkout_url = None

@app.route('/create-checkout', methods=['POST'])
def create_checkout():
    global latest_checkout_url
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
                    'currency': 'sgd',
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
        
        # Store the checkout URL
        latest_checkout_url = session.url
        
        # Open the URL in the default browser
        def open_browser():
            time.sleep(0.5)  # Small delay to ensure the response is sent first
            webbrowser.open(latest_checkout_url)
            
        threading.Thread(target=open_browser).start()
        
        # Return the checkout URL in the response as well
        return jsonify({'url': session.url, 'message': 'Opening checkout page in browser...'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/redirect-to-checkout', methods=['GET'])
def redirect_to_checkout():
    global latest_checkout_url
    if latest_checkout_url:
        return redirect(latest_checkout_url)
    else:
        return "No active checkout session", 400

@app.route('/success')
def success():
    return 'Payment successful!'

@app.route('/cancel')
def cancel():
    return 'Payment canceled.'

if __name__ == '__main__':
    print(f"Server running on http://localhost:{PORT}")
    app.run(host='0.0.0.0', port=PORT, debug=True)

# Navigate to this directory and run python browser.py
# Open another command prompt and use the following command: 
# curl -X POST http://localhost:3000/create-checkout -H "Content-Type: application/json" -d "{\"amount\": 1999, \"description\": \"Test payment\"}"

# Should get a browser popup with checkout details