"""
Market Risk Dashboard

Entry point of the application.
"""

import streamlit as st
import pandas as pd
import plotly.express as px

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

def display_risk_status(
    label: str,
    value: float,
    status: str,
) -> None:
    """Display a risk metric with a colored status indicator."""

    status_color = {
        "Within Limit": "#2ECC71",
        "Warning": "#F4D03F",
        "Breach": "#E74C3C",
    }.get(status, "#95A5A6")

    st.markdown(
        f"""
<div style="
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 10px;
    padding: 16px;
    background-color: rgba(255,255,255,0.02);
">
<div style="font-size: 0.95rem; font-weight: 600;">{label}</div>
<div style="font-size: 1.5rem; font-weight: 700; margin: 8px 0;">{value:.2%}</div>
<div style="display: flex; align-items: center; gap: 8px; font-size: 0.95rem;">
<span style="color: {status_color}; font-size: 1.2rem;">●</span>
<span>{status}</span>
</div>
</div>
""",
        unsafe_allow_html=True,
    )

def main():

    st.set_page_config(
        page_title="Market Risk Dashboard",
        page_icon="📊",
        layout="wide",
    )

    st.markdown(
        """
        <style>
            .block-container {
                padding-top: 2rem;
                padding-bottom: 3rem;
                max-width: 1500px;
            }

            h1 {
                font-size: 2.2rem !important;
                font-weight: 700 !important;
                margin-bottom: 0.3rem !important;
            }

            h2, h3 {
                font-weight: 650 !important;
                margin-top: 1.6rem !important;
                margin-bottom: 0.8rem !important;
            }

            [data-testid="stMetric"] {
                background-color: rgba(255, 255, 255, 0.03);
                border: 1px solid rgba(255, 255, 255, 0.06);
                padding: 1rem 1.1rem;
                border-radius: 10px;
            }

            [data-testid="stMetricLabel"] {
                font-size: 0.9rem;
                opacity: 0.75;
            }

            [data-testid="stMetricValue"] {
                font-size: 1.7rem;
                font-weight: 700;
            }

            [data-testid="stDataFrame"] {
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 8px;
            }

            section[data-testid="stSidebar"] {
                border-right: 1px solid rgba(255, 255, 255, 0.08);
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("Market Risk Dashboard")

    st.sidebar.header("Analysis Settings")

    start_date = st.sidebar.date_input(
        "Start date",
        value=pd.to_datetime("2020-01-01"),
    )

    end_date = st.sidebar.date_input(
        "End date",
        value=pd.to_datetime("2026-01-01"),
    )

    rolling_window = st.sidebar.slider(
        "Rolling volatility window",
        min_value=20,
        max_value=120,
        value=30,
        step=10,
    )

    selected_confidence_level = st.sidebar.selectbox(
        "VaR confidence level",
        options=[0.95, 0.99],
        format_func=lambda x: f"{x:.0%}",
    )

    st.markdown(
        """
        <p style="
            font-size:1.1rem;
            line-height:1.7;
            color:rgba(255,255,255,0.78);
            max-width:850px;
            margin-top:-0.2rem;
            margin-bottom:1.2rem;
        ">
            Interactive dashboard for monitoring portfolio market risk using historical
            market data. The dashboard summarizes portfolio allocation, volatility,
            Value at Risk (VaR), Expected Shortfall (ES), drawdown, and risk limit
            monitoring.
        </p>
        """,
        unsafe_allow_html=True,
    )

    tickers = get_default_tickers()

    print("====================================")
    print("      Market Risk Dashboard")
    print("====================================")

    prices = download_market_data(
        tickers=tickers,
        start_date=str(start_date),
        end_date=str(end_date),
    )

    print(prices.head())

    # Calculate daily returns
    returns = calculate_daily_returns(prices)

    print("\nDaily returns:")
    print(returns.head())

    weights = get_default_weights()

    portfolio_composition = pd.DataFrame(
        {
            "Ticker": list(weights.keys()),
            "Weight": list(weights.values()),
        }
    )

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
    rolling_annualized_volatility = calculate_annualized_rolling_volatility(portfolio_returns, window=rolling_window)

    historical_var_1d = calculate_historical_var_1d(
        portfolio_returns,
        confidence_level=selected_confidence_level,
    )

    historical_var_95_1d = calculate_historical_var_1d(portfolio_returns)
    historical_var_99_1d = calculate_historical_var_1d(
        portfolio_returns,
        confidence_level=0.99,
    )

    historical_es_1d = calculate_historical_expected_shortfall_1d(
        portfolio_returns,
        confidence_level=selected_confidence_level,
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

    st.divider()

    st.subheader("Portfolio Overview")
    st.caption(
        "Fixed portfolio allocation used throughout the analysis period."
    )

    composition_col1, composition_col2 = st.columns(
        [1, 1.15],
        vertical_alignment="top",
    )

    with composition_col1:
        display_weights = portfolio_composition.copy()

        display_weights["Weight"] = display_weights["Weight"].map(
            lambda x: f"{x:.0%}"
        )

        st.dataframe(
            display_weights,
            hide_index=True,
            use_container_width=True,
        )

    with composition_col2:
        portfolio_chart = px.bar(
            portfolio_composition,
            x="Ticker",
            y="Weight",
        )

        portfolio_chart.update_traces(
            width=0.45,
        )

        portfolio_chart.update_yaxes(
            tickformat=".0%",
            range=[0, 0.45],
        )

        portfolio_chart.update_layout(
            height=220,
            margin=dict(
                l=10,
                r=10,
                t=5,
                b=10,
            ),
            xaxis_title=None,
            yaxis_title=None,
            bargap=0.55,
            showlegend=False,
        )

        st.plotly_chart(
            portfolio_chart,
            use_container_width=True,
        )

    st.divider()

    st.subheader("Portfolio Risk Summary")
    st.caption("Headline risk metrics for the selected analysis period.")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Annualized Volatility",
        f"{annualized_volatility:.2%}",
    )

    col2.metric(
        f"{selected_confidence_level:.0%} Historical VaR",
        f"{historical_var_1d:.2%}",
    )

    col3.metric(
        f"{selected_confidence_level:.0%} Expected Shortfall",
        f"{historical_es_1d:.2%}",
    )

    col4.metric(
        "Maximum Drawdown",
        f"{maximum_drawdown:.2%}",
    )

    st.subheader("Risk Limit Monitoring")

    limit_col1, limit_col2, limit_col3 = st.columns(3)

    with limit_col1:
        display_risk_status(
            "Annualized Volatility",
            annualized_volatility,
            volatility_status,
        )

    with limit_col2:
        display_risk_status(
            "95% Historical VaR",
            historical_var_95_1d,
            var_status,
        )

    with limit_col3:
        display_risk_status(
            "Maximum Drawdown",
            maximum_drawdown,
            drawdown_status,
        )

    st.divider()

    st.subheader(
        f"{rolling_window}-Day Rolling Annualized Volatility"
    )

    rolling_volatility_chart = px.line(
        rolling_annualized_volatility.dropna(),
    )

    rolling_volatility_chart.update_layout(
        height=380,
        xaxis_title=None,
        yaxis_title="Annualized Volatility",
        showlegend=False,
        margin=dict(l=20, r=20, t=10, b=20),
    )

    rolling_volatility_chart.update_yaxes(
        tickformat=".0%",
    )

    st.plotly_chart(
        rolling_volatility_chart,
        use_container_width=True,
    )

    st.subheader("Portfolio Drawdown")

    drawdown_chart = px.line(
        drawdown,
    )

    drawdown_chart.update_layout(
        height=380,
        xaxis_title=None,
        yaxis_title="Drawdown",
        showlegend=False,
        margin=dict(l=20, r=20, t=10, b=20),
    )

    drawdown_chart.update_yaxes(
        tickformat=".0%",
    )

    st.plotly_chart(
        drawdown_chart,
        use_container_width=True,
    )

    st.divider()

    st.subheader("Methodology & Assumptions")

    st.markdown(
        """
    ### The dashboard calculates market risk using historical daily portfolio returns and a fixed asset allocation.

    ### Portfolio Construction

    - **Portfolio:** Fixed multi-asset portfolio consisting of:
    - **SPY:** 40%
    - **QQQ:** 30%
    - **TLT:** 20%
    - **GLD:** 10%
    - Portfolio weights remain constant throughout the analysis period.

    ### Market Data

    - Historical daily adjusted closing prices downloaded from **Yahoo Finance**.
    - Analysis period is determined by the selected start and end dates.
    - Daily asset returns are calculated using percentage changes in adjusted closing prices.

    ### Risk Measures

    - **Annualized Volatility:** Daily portfolio volatility annualized using √252 trading days.
    - **Rolling Annualized Volatility:** Calculated over the selected rolling window.
    - **Historical Value at Risk (VaR):** Estimated using the historical simulation approach at the selected confidence level.
    - **Historical Expected Shortfall (ES):** Average portfolio loss beyond the historical VaR threshold.
    - **Maximum Drawdown:** Largest peak-to-trough decline in cumulative portfolio returns.

    ### Risk Limits

    - Portfolio risk metrics are compared against predefined risk thresholds.
    - Risk limits are included for demonstration purposes and do not represent regulatory or institutional risk limits.
    """
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