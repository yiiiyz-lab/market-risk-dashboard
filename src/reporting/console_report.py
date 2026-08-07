"""Console reporting for the Market Risk Dashboard."""


def print_risk_summary(
    daily_volatility: float,
    annualized_volatility: float,
    historical_var_95_1d: float,
    historical_var_99_1d: float,
    historical_es_95_1d: float,
    historical_es_99_1d: float,
    maximum_drawdown: float,
) -> None:
    """Print core portfolio risk metrics."""

    print("\nPortfolio Risk Summary:")
    print(f"- Daily volatility: {daily_volatility:.2%}")
    print(f"- Annualized volatility: {annualized_volatility:.2%}")
    print(f"- 95% Historical VaR: {historical_var_95_1d:.2%}")
    print(f"- 99% Historical VaR: {historical_var_99_1d:.2%}")
    print(f"- 95% Historical ES: {historical_es_95_1d:.2%}")
    print(f"- 99% Historical ES: {historical_es_99_1d:.2%}")
    print(f"- Maximum drawdown: {maximum_drawdown:.2%}")

def print_risk_limit_summary(
    annualized_volatility: float,
    volatility_status: str,
    historical_var_95_1d: float,
    var_status: str,
    maximum_drawdown: float,
    drawdown_status: str,
) -> None:
    """Print risk limit monitoring results."""

    print("\nRisk Limit Monitoring:")
    print(
        f"- Annualized volatility: "
        f"{annualized_volatility:.2%} | {volatility_status}"
    )
    print(
        f"- 95% Historical VaR: "
        f"{historical_var_95_1d:.2%} | {var_status}"
    )
    print(
        f"- Maximum drawdown: "
        f"{maximum_drawdown:.2%} | {drawdown_status}"
    )

def print_rolling_volatility_summary(
    rolling_annualized_volatility,
) -> None:
    """Print recent rolling annualized volatility."""

    print("\nRolling Annualized Volatility:")

    print(
        rolling_annualized_volatility
        .dropna()
        .tail()
        .map(lambda x: f"{x:.2%}")
    )