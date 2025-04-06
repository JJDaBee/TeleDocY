from flask import Flask, request, jsonify
import stripe  # type: ignore
import os

app = Flask(__name__)

# Set your Stripe secret key from environment variable
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

@app.route('/create-checkout', methods=['POST'])
def create_checkout():
    try:
        data = request.get_json()
        amount = data.get('amount')  # in cents
        description = data.get('description', 'Payment')

        if not amount:
            return jsonify({"error": "Missing amount"}), 400

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            mode='payment',
            line_items=[{
                'price_data': {
                    'currency': 'sgd',
                    'product_data': {'name': description},
                    'unit_amount': amount,
                },
                'quantity': 1,
            }],
            success_url="http://localhost:3001/success",
            cancel_url="http://localhost:3001/cancel",
        )

        return jsonify({
            "url": session.url,
            "message": "Stripe checkout session created successfully."
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/success')
def success():
    return '✅ Payment successful!'

@app.route('/cancel')
def cancel():
    return '❌ Payment canceled.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3001, debug=True)
