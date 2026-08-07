"""Volatility calculations for portfolio risk analysis."""

import numpy as np
import pandas as pd


TRADING_DAYS = 252
ROLLING_WINDOW = 30


def calculate_daily_volatility(
    portfolio_returns: pd.Series,
) -> float:
    """Calculate the standard deviation of daily portfolio returns."""

    return portfolio_returns.std()


def calculate_annualized_volatility(
    portfolio_returns: pd.Series,
) -> float:
    """Calculate annualized portfolio volatility."""

    daily_volatility = calculate_daily_volatility(portfolio_returns)

    return daily_volatility * np.sqrt(TRADING_DAYS)

def calculate_annualized_rolling_volatility(
    portfolio_returns: pd.Series,
    window: int = ROLLING_WINDOW,
) -> pd.Series:
    """Calculate rolling annualized portfolio volatility."""

    rolling_daily_volatility = portfolio_returns.rolling(
        window=window
    ).std()

    return rolling_daily_volatility * np.sqrt(TRADING_DAYS)