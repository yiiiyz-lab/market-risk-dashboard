"""Drawdown calculations for portfolio risk analysis."""

import pandas as pd

def calculate_drawdown(
    portfolio_returns: pd.Series,
) -> pd.Series:
    """Calculate the portfolio drawdown series."""

    cumulative_growth = (1 + portfolio_returns).cumprod()

    running_peak = cumulative_growth.cummax()

    drawdown = cumulative_growth / running_peak - 1

    return drawdown


def calculate_maximum_drawdown(
    portfolio_returns: pd.Series,
) -> float:
    """Calculate the maximum portfolio drawdown."""

    drawdown = calculate_drawdown(portfolio_returns)

    return -drawdown.min()