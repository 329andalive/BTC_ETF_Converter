import yfinance as yf
from flask import Flask, render_template, request
import datetime

# Create our Flask web server
app = Flask(__name__)

# Define the list of ETFs we want to support
ETF_TICKERS = ['IBIT', 'FBTC', 'ARKB', 'BITB', 'GBTC']

@app.route('/')
def home():
    """
    This route gets prices for BTC and a selected ETF, and handles the hypothetical calculator.
    """
    # Get the user's ETF choice from the URL. Default to 'IBIT' if none is selected.
    selected_etf = request.args.get('etf_choice', default='IBIT')
    if selected_etf not in ETF_TICKERS:
        selected_etf = 'IBIT' # Fallback for safety

    btc_price = 0
    etf_price = 0 # Changed from ibit_price to be generic
    error_message = None
    hypothetical_etf_price = None # Changed from hypothetical_ibit_price

    try:
        # --- Part 1: Fetch Live Prices ---
        btc_ticker = yf.Ticker("BTC-USD")
        etf_ticker = yf.Ticker(selected_etf) # Use the selected ETF ticker

        btc_data = btc_ticker.history(period='1d')
        etf_data = etf_ticker.history(period='1d')

        if not btc_data.empty and not etf_data.empty:
            btc_price = btc_data['Close'].iloc[-1]
            etf_price = etf_data['Close'].iloc[-1]
        else:
            error_message = "Could not retrieve live price data."

        # --- Part 2: Handle the Hypothetical Calculator ---
        hypothetical_btc_str = request.args.get('hypothetical_btc')

        if hypothetical_btc_str and btc_price > 0:
            try:
                hypothetical_btc_price = float(hypothetical_btc_str)
                # Calculate the ratio using the live prices we just fetched
                live_ratio = etf_price / btc_price
                # Apply the ratio to the user's hypothetical BTC price
                hypothetical_etf_price = hypothetical_btc_price * live_ratio
            except (ValueError, ZeroDivisionError):
                pass # Fail silently if input is bad or prices are zero

    except Exception as e:
        error_message = f"An error occurred: {e}"

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S EST")

    # Render the HTML page, passing the generic variables and the list of ETFs
    return render_template(
        'index.html',
        btc_price=btc_price,
        etf_price=etf_price, # Generic name
        timestamp=timestamp,
        error=error_message,
        hypothetical_etf_price=hypothetical_etf_price, # Generic name
        etf_tickers=ETF_TICKERS, # Pass the whole list for the dropdown
        selected_etf=selected_etf # Pass the currently selected one
    )

if __name__ == '__main__':
    app.run(debug=True)