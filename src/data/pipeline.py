"""
src/data/pipeline.py
Fetches live options data and builds calibrated SVI volatility surfaces.
"""

import numpy as np
import pandas as pd
import yfinance as yf
from src.models.svi import calibrate_svi_smile, svi_implied_volatility


def fetch_and_calibrate_surface(ticker_symbol: str = "SPY", r: float = 0.045):
    """Fetches real-time market options chain and calibrates SVI across all expiries."""
    ticker = yf.Ticker(ticker_symbol)
    underlying_price = ticker.fast_info["lastPrice"]
    
    # FIXED: yfinance uses 'options' instead of 'expirations'
    expirations = ticker.options[:6]  # First 6 maturities

    surface_data = []

    print(f"Fetching options for {ticker_symbol} (Spot: ${underlying_price:.2f})...")

    for exp in expirations:
        opt = ticker.option_chain(exp)
        calls = opt.calls.dropna(subset=["impliedVolatility"])

        # Calculate time to maturity T in years
        today = pd.Timestamp.now()
        T = max((pd.Timestamp(exp) - today).days / 365.25, 0.005)

        # Forward price approx: F = S * exp(r * T)
        F = underlying_price * np.exp(r * T)

        # Filter out deep OTM/ITM or low volume options for clean calibration
        filtered = calls[
            (calls["strike"] >= underlying_price * 0.7) & 
            (calls["strike"] <= underlying_price * 1.3) & 
            (calls["impliedVolatility"] > 0.02)
        ].copy()

        if len(filtered) < 5:
            continue

        strikes = filtered["strike"].values
        market_ivs = filtered["impliedVolatility"].values
        log_moneyness = np.log(strikes / F)

        # Calibrate SVI
        svi_params, loss = calibrate_svi_smile(log_moneyness, market_ivs, T)

        # Generate smooth fitted curve for visualization
        smooth_k = np.linspace(log_moneyness.min(), log_moneyness.max(), 50)
        smooth_strikes = F * np.exp(smooth_k)
        fitted_ivs = svi_implied_volatility(smooth_k, T, svi_params)

        for K, iv in zip(smooth_strikes, fitted_ivs):
            surface_data.append({
                "T": T,
                "Expiration": exp,
                "Strike": K,
                "LogMoneyness": np.log(K / F),
                "SVI_IV": iv
            })

    return pd.DataFrame(surface_data), underlying_price