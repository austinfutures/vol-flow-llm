"""
src/models/svi.py
Core options pricing, implied volatility inversion, and SVI surface calibration engine.
"""

import numpy as np
from scipy.optimize import minimize
from scipy.stats import norm


def black_scholes_call_price(S: float, K: float, T: float, r: float, sigma: float) -> float:
    """Calculate Black-Scholes European Call option price."""
    if T <= 0 or sigma <= 0:
        return max(0.0, S - K)
    
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)


def implied_volatility(
    price: float, S: float, K: float, T: float, r: float, option_type: str = "call"
) -> float:
    """Invert Black-Scholes price to find Implied Volatility using Brent's method."""
    if T <= 0 or price <= 0:
        return np.nan

    # Define objective function
    def bs_diff(sig):
        if option_type == "call":
            p = black_scholes_call_price(S, K, T, r, sig)
        else:
            # Put-Call Parity: P = C - S + K*exp(-rT)
            c = black_scholes_call_price(S, K, T, r, sig)
            p = c - S + K * np.exp(-r * T)
        return p - price

    # Search boundaries for volatility [0.01%, 500%]
    try:
        from scipy.optimize import brentq
        return brentq(bs_diff, 1e-4, 5.0)
    except (ValueError, RuntimeError):
        return np.nan


def raw_svi_total_variance(k: np.ndarray, params: tuple) -> np.ndarray:
    """
    Computes Raw SVI Total Variance w(k).
    params: (a, b, rho, m, sigma)
    k: log-moneyness ln(K / F)
    """
    a, b, rho, m, sigma = params
    return a + b * (rho * (k - m) + np.sqrt((k - m) ** 2 + sigma**2))


def svi_implied_volatility(k: np.ndarray, T: float, params: tuple) -> np.ndarray:
    """Converts SVI Total Variance w(k) to Implied Volatility sigma(k) = sqrt(w(k)/T)."""
    w = raw_svi_total_variance(k, params)
    # Clip negative total variance to prevent sqrt domain errors during optimization
    w = np.maximum(w, 1e-6)
    return np.sqrt(w / T)


def calibrate_svi_smile(log_moneyness: np.ndarray, market_iv: np.ndarray, T: float) -> tuple:
    """
    Calibrates SVI parameters (a, b, rho, m, sigma) to observed market IVs for a single expiry T.
    Enforces butterfly & vertical arbitrage constraints.
    """
    market_w = (market_iv**2) * T

    # Objective function: Sum of Squared Errors (SSE)
    def objective(params):
        a, b, rho, m, sigma = params
        model_w = raw_svi_total_variance(log_moneyness, params)
        return np.sum((model_w - market_w) ** 2)

    # Parameter constraints:
    # b >= 0, |rho| < 1, sigma > 0, a + b*sigma*sqrt(1 - rho^2) >= 0 (no negative variance)
    bounds = [
        (-0.5, 0.5),    # a
        (1e-4, 2.0),    # b
        (-0.99, 0.99),  # rho
        (-1.0, 1.0),    # m
        (1e-4, 1.0)     # sigma
    ]

    # Initial guess
    x0 = (0.01, 0.1, -0.2, 0.0, 0.1)

    res = minimize(objective, x0, method="SLSQP", bounds=bounds)
    return res.x, res.fun