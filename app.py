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

from src.risk.var import (
    calculate_historical_var_1d
)

from src.risk.expected_shortfall import (
    calculate_historical_expected_shortfall_1d,
)

from src.risk.drawdown import (
    calculate_drawdown,
    calculate_maximum_drawdown,
)

from src.risk.limits import (
    DRAWDOWN_LIMIT,
    VAR_95_LIMIT,
    VOLATILITY_LIMIT,
    evaluate_risk_limit,
)

from src.reporting.console_report import (
    print_risk_limit_summary,
    print_risk_summary,
    print_rolling_volatility_summary,
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

    historical_var_95_1d = calculate_historical_var_1d(portfolio_returns)
    historical_var_99_1d = calculate_historical_var_1d(
        portfolio_returns,
        confidence_level=0.99,
    )

    historical_es_95_1d = calculate_historical_expected_shortfall_1d(portfolio_returns)
    historical_es_99_1d = calculate_historical_expected_shortfall_1d(
        portfolio_returns,
        confidence_level=0.99,
    )

    drawdown = calculate_drawdown(portfolio_returns)
    maximum_drawdown = calculate_maximum_drawdown(portfolio_returns)

    volatility_status = evaluate_risk_limit(
        annualized_volatility,
        VOLATILITY_LIMIT,
    )

    var_status = evaluate_risk_limit(
        historical_var_95_1d,
        VAR_95_LIMIT,
    )

    drawdown_status = evaluate_risk_limit(
        maximum_drawdown,
        DRAWDOWN_LIMIT,
    )

    print_risk_summary(
        daily_volatility=daily_volatility,
        annualized_volatility=annualized_volatility,
        historical_var_95_1d=historical_var_95_1d,
        historical_var_99_1d=historical_var_99_1d,
        historical_es_95_1d=historical_es_95_1d,
        historical_es_99_1d=historical_es_99_1d,
        maximum_drawdown=maximum_drawdown,
    )

    print_rolling_volatility_summary(
        rolling_annualized_volatility,
    )

    print_risk_limit_summary(
        annualized_volatility=annualized_volatility,
        volatility_status=volatility_status,
        historical_var_95_1d=historical_var_95_1d,
        var_status=var_status,
        maximum_drawdown=maximum_drawdown,
        drawdown_status=drawdown_status,
    )

if __name__ == "__main__":
    main()