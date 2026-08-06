"""Portfolio construction and return calculations."""

import pandas as pd


def get_default_weights() -> dict[str, float]:
    """Return the default portfolio weights."""
    return {
        "SPY": 0.40,
        "QQQ": 0.30,
        "TLT": 0.20,
        "GLD": 0.10,
    }


def calculate_portfolio_returns(
    asset_returns: pd.DataFrame,
    weights: dict[str, float],
) -> pd.Series:
    """Calculate weighted daily portfolio returns."""

    if abs(sum(weights.values()) - 1.0) > 1e-10:
        raise ValueError("Portfolio weights must sum to 1.0.")

    missing_tickers = set(weights) - set(asset_returns.columns)

    if missing_tickers:
        raise ValueError(
            f"Missing return data for: {sorted(missing_tickers)}"
        )

    ordered_returns = asset_returns[list(weights)]
    weight_series = pd.Series(weights)

    return ordered_returns.mul(weight_series).sum(axis=1)