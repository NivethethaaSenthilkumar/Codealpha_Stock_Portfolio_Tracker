# Importing required libraries
import requests
import matplotlib.pyplot as plt
import pandas as pd
def fetch_stock_data(symbol, api_key):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    return data
def process_stock_data(data):
    time_series = data["Time Series (Daily)"]
    dates = []
    prices = []
    for date, stats in time_series.items():
        dates.append(date)
        prices.append(float(stats["4. close"]))
    
    df = pd.DataFrame({"Date": dates, "Close Price": prices})
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date")
    return df
def plot_stock_data(df, symbol):
    plt.figure(figsize=(10, 5))
    plt.plot(df["Date"], df["Close Price"], label=symbol)
    plt.xlabel("Date")
    plt.ylabel("Close Price")
    plt.title(f"{symbol} Stock Price Over Time")
    plt.legend()
    plt.show()
portfolio = {}

def add_stock_to_portfolio(symbol, shares, purchase_price):
    portfolio[symbol] = {"shares": shares, "purchase_price": purchase_price}

def remove_stock_from_portfolio(symbol):
    if symbol in portfolio:
        del portfolio[symbol]

def update_stock_in_portfolio(symbol, shares, purchase_price):
    if symbol in portfolio:
        portfolio[symbol]["shares"] = shares
        portfolio[symbol]["purchase_price"] = purchase_price

def calculate_portfolio_value():
    total_value = 0
    for symbol, details in portfolio.items():
        data = fetch_stock_data(symbol, api_key)
        df = process_stock_data(data)
        latest_price = df["Close Price"].iloc[-1]
        total_value += latest_price * details["shares"]
    return total_value
# Replace with your API key
api_key = "YOUR_API_KEY"

# Add stocks to your portfolio
add_stock_to_portfolio("AAPL", 10, 150)
add_stock_to_portfolio("MSFT", 5, 250)

# Calculate total portfolio value
total_value = calculate_portfolio_value()
print(f"Total Portfolio Value: ${total_value:.2f}")

# Plot stock data for each stock in the portfolio
for symbol in portfolio.keys():
    data = fetch_stock_data(symbol, api_key)
    df = process_stock_data(data)
    plot_stock_data(df, symbol)
