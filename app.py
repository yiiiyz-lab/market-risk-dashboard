"""
Market Risk Dashboard

Entry point of the application.
"""

from src.data.market_data import (
    calculate_daily_returns,
    get_default_tickers,
    download_market_data,
)

from src.portfolio.portfolio import (
    calculate_portfolio_returns,
    get_default_weights,
)

def main():

    tickers = get_default_tickers()

    print("====================================")
    print("      Market Risk Dashboard")
    print("====================================")

    prices = download_market_data(
        tickers=tickers,
        start_date="2020-01-01",
        end_date="2026-07-31",
    )

    print(prices.head())

    # Calculate daily returns
    returns = calculate_daily_returns(prices)

    print("\nDaily returns:")
    print(returns.head())

    weights = get_default_weights()

    portfolio_returns = calculate_portfolio_returns(
        asset_returns=returns,
        weights=weights,
    )

    print("\nPortfolio weights:")

    for ticker, weight in weights.items():
        print(f"- {ticker}: {weight:.0%}")

    print("\nPortfolio returns:")
    print(portfolio_returns.head())

if __name__ == "__main__":
    main()