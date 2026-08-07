"""Historical Value at Risk calculations."""

import pandas as pd

CONFIDENCE_LEVEL = 0.95

def calculate_historical_var_1d(
    portfolio_returns: pd.Series,
    confidence_level: float = CONFIDENCE_LEVEL,
) -> float:
    """Calculate historical Value at Risk as a positive loss value."""

    percentile = 1 - confidence_level
    var_return = portfolio_returns.quantile(percentile)

    return -var_return