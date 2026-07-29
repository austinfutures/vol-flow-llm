# vol-flow-llm

> **SVI Volatility Surface Modeling, Delta-Hedged Dispersion Backtester, and LLM News Parser.**

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

```text
vol-flow-llm/
│
├── main.py
├── requirements.txt
├── README.md
│
└── src/
    ├── data/
    │   └── pipeline.py
    └── models/
        └── svi.py
