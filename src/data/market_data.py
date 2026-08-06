"""
Market data module.

This module defines the market instruments used in the sample portfolio.
"""


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