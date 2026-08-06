"""
Market Risk Dashboard

Entry point of the application.
"""

from src.data.market_data import get_default_tickers

def main():

    tickers = get_default_tickers()

    print("====================================")
    print("      Market Risk Dashboard")
    print("====================================")
    print("Portfolio instruments:")

    for ticker in tickers:
        print(f"- {ticker}")


if __name__ == "__main__":
    main()