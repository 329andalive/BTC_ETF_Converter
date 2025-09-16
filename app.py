import yfinance as yf
from flask import Flask, render_template
import datetime

# Create our Flask web server
app = Flask(__name__)

@app.route('/')
def home():
    """
    This is the main route of our web app. It gets the prices and displays them.
    """
    btc_price = 0
    ibit_price = 0
    error_message = None

    try:
        # Define the tickers for Bitcoin (BTC-USD) and iShares Bitcoin Trust (IBIT)
        btc_ticker = yf.Ticker("BTC-USD")
        ibit_ticker = yf.Ticker("IBIT")

        # Get the most recent price data. We use history() to get the last day's data
        # and grab the last closing price from that.
        btc_data = btc_ticker.history(period='1d')
        ibit_data = ibit_ticker.history(period='1d')

        if not btc_data.empty and not ibit_data.empty:
            btc_price = btc_data['Close'].iloc[-1]
            ibit_price = ibit_data['Close'].iloc[-1]
        else:
            error_message = "Could not retrieve price data. The market may be closed or data is unavailable."

    except Exception as e:
        # If anything goes wrong during the API call, we'll show an error.
        error_message = f"An error occurred: {e}"

    # Get the current time for our 'Last updated' timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S EST")

    # Render the HTML page and pass the variables to it
    return render_template(
        'index.html',
        btc_price=btc_price,
        ibit_price=ibit_price,
        timestamp=timestamp,
        error=error_message
    )

if __name__ == '__main__':
    # This block allows us to run the app locally for testing
    app.run(debug=True)