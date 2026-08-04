import numpy as np
import pandas as pd


TRADING_DAYS_PER_YEAR = 252


def calculate_cagr(equity: pd.Series) -> float:
    """Calculate compound annual growth rate."""

    clean_equity = equity.dropna()

    if len(clean_equity) < 2:
        raise ValueError("Equity series must contain at least two values.")

    years = (
        clean_equity.index[-1] - clean_equity.index[0]
    ).days / 365.25

    if years <= 0:
        raise ValueError("Equity series must span a positive time period.")

    return (clean_equity.iloc[-1] / clean_equity.iloc[0]) ** (1 / years) - 1


def calculate_max_drawdown(equity: pd.Series) -> float:
    """Calculate maximum drawdown."""

    running_max = equity.cummax()
    drawdown = equity / running_max - 1

    return drawdown.min()


def calculate_annual_volatility(returns: pd.Series) -> float:
    """Calculate annualized volatility."""

    return returns.std() * np.sqrt(TRADING_DAYS_PER_YEAR)


def calculate_sharpe_ratio(
    returns: pd.Series,
    risk_free_rate: float = 0.0,
) -> float:
    """Calculate annualized Sharpe ratio."""

    clean_returns = returns.dropna()

    annual_return = clean_returns.mean() * TRADING_DAYS_PER_YEAR
    annual_volatility = calculate_annual_volatility(clean_returns)

    if annual_volatility == 0:
        return 0.0

    return (annual_return - risk_free_rate) / annual_volatility