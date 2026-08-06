"""
Market data module.

This module defines the market instruments used in the sample portfolio.
"""

import yfinance as yf
import pandas as pd

def get_default_tickers() -> list[str]:
    """
    Return the default portfolio instruments.
    """

    return [
        "SPY",   # US equities
        "QQQ",   # Nasdaq 100
        "TLT",   # Long-term US Treasury bonds
        "GLD"    # Gold
    ]

def download_market_data(
    tickers: list[str],
    start_date: str,
    end_date: str,
) -> pd.DataFrame:
    """
    Download historical adjusted closing prices from Yahoo Finance.
    """

    prices = yf.download(
        tickers,
        start=start_date,
        end=end_date,
        auto_adjust=True,
        progress=False,
    )

    return prices["Close"]

def calculate_daily_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate daily percentage returns from historical prices.
    """
    returns = prices.pct_change()
    return returns.dropna()