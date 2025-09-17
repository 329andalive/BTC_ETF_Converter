import yfinance as yf
from flask import Flask, render_template, request # 'request' is new!
import datetime

# Create our Flask web server
app = Flask(__name__)

@app.route('/')
def home():
    """
    This is the main route of our web app. It gets the prices and displays them.
    It now also handles the hypothetical price calculation.
    """
    btc_price = 0
    ibit_price = 0
    error_message = None
    hypothetical_ibit_price = None # This is for our new feature

    try:
        # --- Part 1: Fetch Live Prices (Same as before) ---
        btc_ticker = yf.Ticker("BTC-USD")
        ibit_ticker = yf.Ticker("IBIT")

        btc_data = btc_ticker.history(period='1d')
        ibit_data = ibit_ticker.history(period='1d')

        if not btc_data.empty and not ibit_data.empty:
            btc_price = btc_data['Close'].iloc[-1]
            ibit_price = ibit_data['Close'].iloc[-1]
        else:
            error_message = "Could not retrieve live price data."

        # --- Part 2: Handle the Hypothetical Calculator (NEW!) ---
        # request.args.get() reads the value from the form input box in the URL
        hypothetical_btc_str = request.args.get('hypothetical_btc')

        if hypothetical_btc_str and ibit_price > 0:
            try:
                # Convert user input to a number
                hypothetical_btc_price = float(hypothetical_btc_str)
                
                # Calculate the ratio between live prices
                live_ratio = ibit_price / btc_price
                
                # Apply that ratio to the user's hypothetical BTC price
                hypothetical_ibit_price = hypothetical_btc_price * live_ratio
                
            except (ValueError, ZeroDivisionError):
                # If user types "abc" or if live prices are zero, do nothing
                pass

    except Exception as e:
        error_message = f"An error occurred: {e}"

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S EST")

    # Render the HTML page and pass ALL the variables to it, including the new one
    return render_template(
        'index.html',
        btc_price=btc_price,
        ibit_price=ibit_price,
        timestamp=timestamp,
        error=error_message,
        hypothetical_ibit_price=hypothetical_ibit_price # Pass the new variable
    )

if __name__ == '__main__':
    app.run(debug=True)