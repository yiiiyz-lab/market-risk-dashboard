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

from src.risk.volatility import (
    calculate_annualized_rolling_volatility,
    calculate_annualized_volatility,
    calculate_daily_volatility,
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

    daily_volatility = calculate_daily_volatility(portfolio_returns)
    annualized_volatility = calculate_annualized_volatility(portfolio_returns)
    rolling_annualized_volatility = calculate_annualized_rolling_volatility(portfolio_returns)

    print("\nPortfolio volatility:")
    print(f"- Daily volatility: {daily_volatility:.2%}")
    print(f"- Annualized volatility: {annualized_volatility:.2%}")

    print("\nRolling annualized volatility:")
    print(rolling_annualized_volatility.dropna().head().map(lambda x: f"{x:.2%}"))

    print("\nRolling annualized volatility (last 5):")
    print(rolling_annualized_volatility.dropna().tail().map(lambda x: f"{x:.2%}"))

if __name__ == "__main__":
    main()