"""Risk limit monitoring for portfolio risk metrics."""

from dataclasses import dataclass

@dataclass
class RiskLimit:
    """Define warning and breach thresholds for a risk metric."""

    warning: float
    breach: float


VOLATILITY_LIMIT = RiskLimit(
    warning=0.18,
    breach=0.22,
)

VAR_95_LIMIT = RiskLimit(
    warning=0.02,
    breach=0.03,
)

DRAWDOWN_LIMIT = RiskLimit(
    warning=0.20,
    breach=0.30,
)


def evaluate_risk_limit(
    value: float,
    risk_limit: RiskLimit,
) -> str:
    """Evaluate a risk metric against its warning and breach limits."""

    if value >= risk_limit.breach:
        return "Breach"

    if value >= risk_limit.warning:
        return "Warning"

    return "Within Limit"