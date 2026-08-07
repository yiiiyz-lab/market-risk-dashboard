"""Historical Expected Shortfall calculations."""

import pandas as pd

CONFIDENCE_LEVEL = 0.95

def calculate_historical_expected_shortfall_1d(
    portfolio_returns: pd.Series,
    confidence_level: float = CONFIDENCE_LEVEL,
) -> float:
    """Calculate one-day historical Expected Shortfall."""

    percentile = 1 - confidence_level
    var_threshold = portfolio_returns.quantile(percentile)

    tail_returns = portfolio_returns[
        portfolio_returns <= var_threshold
    ]

    return -tail_returns.mean()