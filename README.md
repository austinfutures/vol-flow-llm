# vol-flow-llm
SVI Volatility Surface Modeling, Delta-Hedged Dispersion Backtester, and LLM News Parser.
# SVI Volatility Surface Calibration

A Python project that fetches live options data from Yahoo Finance, calibrates a Stochastic Volatility Inspired (SVI) volatility smile for multiple option expirations, and visualizes the resulting implied volatility surface in an interactive 3D Plotly graph.

---

## Overview

This project demonstrates how quantitative finance techniques can be combined with real-time market data to construct a smooth implied volatility surface. Instead of relying directly on noisy market implied volatilities, the application fits the Raw SVI parameterization to each option expiration, producing an arbitrage-aware approximation of the volatility smile.

The final output is a three-dimensional volatility surface where:

- **X-axis:** Strike Price
- **Y-axis:** Time to Expiration
- **Z-axis:** SVI Fitted Implied Volatility

---

## Features

- Live options data from Yahoo Finance
- Automatic retrieval of multiple option expirations
- Black-Scholes pricing implementation
- Numerical implied volatility inversion
- Raw SVI volatility smile calibration
- Optimization using SciPy
- Interactive 3D volatility surface visualization
- Modular project structure

---

## Project Structure

```
project/
│
├── main.py
│
├── src/
│   ├── data/
│   │   └── pipeline.py
│   │
│   └── models/
│       └── svi.py
│
├── requirements.txt
└── README.md
```

---

## Mathematical Background

### Black-Scholes Pricing

European call options are priced using the Black-Scholes model:

\[
C = SN(d_1)-Ke^{-rT}N(d_2)
\]

where

\[
d_1=\frac{\ln(S/K)+(r+\sigma^2/2)T}{\sigma\sqrt{T}}
\]

\[
d_2=d_1-\sigma\sqrt{T}
\]

---

### Raw SVI Parameterization

The project uses the Raw SVI formulation for total implied variance:

\[
w(k)=a+b\left[\rho(k-m)+\sqrt{(k-m)^2+\sigma^2}\right]
\]

where

- \(a\) controls overall variance level
- \(b\) controls smile slope
- \(\rho\) controls skew
- \(m\) shifts the smile horizontally
- \(\sigma\) controls curvature

Implied volatility is recovered from total variance:

\[
IV(k)=\sqrt{\frac{w(k)}{T}}
\]

---

## Calibration Process

For each expiration:

1. Download the option chain.
2. Remove invalid or illiquid contracts.
3. Compute forward price approximation.
4. Convert strikes into log-moneyness.
5. Minimize squared error between market variance and SVI variance.
6. Generate a smooth volatility smile.
7. Repeat for all maturities.
8. Assemble the complete volatility surface.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/svi-volatility-surface.git

cd svi-volatility-surface
```

Install dependencies:

```bash
pip install -r requirements.txt
```

or

```bash
pip install numpy pandas scipy plotly yfinance
```

---

## Running

Execute:

```bash
python main.py
```

The program will:

1. Download current option chains.
2. Fit SVI parameters.
3. Construct the volatility surface.
4. Launch an interactive Plotly visualization.

---

## Example Output

```
Fetching options for SPY (Spot: $643.72)...

Calibration Complete.

Rendered 300 fitted surface grid points.
```

An interactive browser window will display a 3D implied volatility surface.

---

## Dependencies

- Python 3.10+
- NumPy
- Pandas
- SciPy
- Plotly
- yfinance

---

## Future Improvements

Potential enhancements include:

- Put option calibration
- Dividend-adjusted forward pricing
- Arbitrage-free SVI parameter constraints
- Full SSVI implementation
- Local volatility surface generation
- SABR comparison
- Heston model calibration
- Surface interpolation across maturities
- Real-time streaming updates
- Interactive Dash web application

---

## Disclaimer

This project is intended for educational and research purposes. Market data obtained from Yahoo Finance may contain inaccuracies or delays and should not be relied upon for trading or investment decisions.

---
