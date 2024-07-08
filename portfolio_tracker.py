import requests

# Replace with your actual Alpha Vantage API key
API_KEY = 'YOUR_ALPHA_VANTAGE_API_KEY'

# Portfolio dictionary to store stock symbol and shares
portfolio = {}

def get_stock_data(symbol):
    """Fetch real-time stock data from Alpha Vantage."""
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=1min&apikey={API_KEY}'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        data = response.json()
        if 'Time Series (1min)' not in data:
            print(f"Error fetching data for {symbol}: {data.get('Note', 'Unknown error')}")
            return None
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

def add_stock(symbol, shares):
    """Add a stock to the portfolio."""
    if symbol in portfolio:
        portfolio[symbol] += shares
    else:
        portfolio[symbol] = shares

def remove_stock(symbol, shares):
    """Remove a stock from the portfolio."""
    if symbol in portfolio:
        if portfolio[symbol] > shares:
            portfolio[symbol] -= shares
        else:
            del portfolio[symbol]

def get_portfolio_value():
    """Calculate the total value of the portfolio."""
    total_value = 0
    for symbol, shares in portfolio.items():
        data = get_stock_data(symbol)
        if data:
            latest_time = max(data['Time Series (1min)'])
            latest_price = float(data['Time Series (1min)'][latest_time]['4. close'])
            total_value += latest_price * shares
    return total_value

def main():
    """Main function to handle user interface."""
    while True:
        print("\nStock Portfolio Tracker")
        print("1. Add Stock")
        print("2. Remove Stock")
        print("3. View Portfolio")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            symbol = input("Enter stock symbol: ").upper()
            try:
                shares = int(input("Enter number of shares: "))
                if shares <= 0:
                    raise ValueError
                add_stock(symbol, shares)
            except ValueError:
                print("Invalid number of shares. Please enter a positive integer.")
        elif choice == '2':
            symbol = input("Enter stock symbol: ").upper()
            try:
                shares = int(input("Enter number of shares: "))
                if shares <= 0:
                    raise ValueError
                remove_stock(symbol, shares)
            except ValueError:
                print("Invalid number of shares. Please enter a positive integer.")
        elif choice == '3':
            value = get_portfolio_value()
            print(f"Total portfolio value: ${value:.2f}")
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
