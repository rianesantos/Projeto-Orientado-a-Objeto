from flask import Flask, jsonify
from flask_cors import CORS  # type: ignore
import requests

app = Flask(__name__)
CORS(app)

ALPHA_VANTAGE_API_KEY = 'f8fc5b4b559e4e83ad08d8be460d3ce1'
SYMBOL = 'IBM'

last_price = None
ALERT_ACTIVE = False

@app.route('/api/data', methods=['GET'])
def get_market_data():

    global last_price, ALERT_ACTIVE

    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={SYMBOL}&apikey={ALPHA_VANTAGE_API_KEY}'

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        quote = data.get('Global Quote', {})
        if not quote:
            return jsonify({'error': 'Data not found or API offline'}), 404

        current_price = float(quote.get('05. price'))

        # Simple alert logic
        alert_triggered = False
        alert_message = None

        # First time: just store the price
        if last_price is None:
            last_price = current_price

        # Check for significant price change
        else:
            if abs(current_price - last_price) >= 1.0:  # If price changes by more than 1.00
                alert_message = f'ALERT! {SYMBOL} price changed from {last_price} to {current_price}!'
                alert_triggered = True
                last_price = current_price

        market_data = {
            'symbol': quote.get('01. symbol'),
            'open': quote.get('02. open'),
            'high': quote.get('03. high'),
            'low': quote.get('04. low'),
            'price': current_price,
            'volume': quote.get('06. volume'),
            'latest_trading_day': quote.get('07. latest trading day')
        }

        return jsonify({
            'data': market_data,
            'alert': {'triggered': alert_triggered, 'message': alert_message}
        })

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Error requesting API: {e}'}), 500
    except (ValueError, TypeError) as e:
        return jsonify({'error': f'Error processing data: {e}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
