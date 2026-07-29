"""
main.py
Execution entry point: Fetches options data, calibrates SVI, and renders 3D Volatility Surface.
"""

import numpy as np
import plotly.graph_objects as go
from scipy.interpolate import griddata
from src.data.pipeline import fetch_and_calibrate_surface


def plot_3d_surface(df, ticker_symbol):
    """Renders interactive 3D SVI Implied Volatility Surface using regular grid interpolation."""
    if df.empty:
        print("Error: No surface data was generated.")
        return

    # Extract coordinates
    strikes = df["Strike"].values
    expiries = df["T"].values
    volatilities = df["SVI_IV"].values

    # Define a uniform 2D grid for plotting
    grid_x = np.linspace(strikes.min(), strikes.max(), 50)  # Strikes axis
    grid_y = np.linspace(expiries.min(), expiries.max(), 30)  # Expiration axis
    grid_x_mesh, grid_y_mesh = np.meshgrid(grid_x, grid_y)

    # Interpolate scattered SVI points onto the uniform grid
    grid_z = griddata(
        (strikes, expiries),
        volatilities,
        (grid_x_mesh, grid_y_mesh),
        method="cubic"
    )

    # Fallback to linear interpolation for boundary NaNs if needed
    if np.isnan(grid_z).any():
        grid_z_linear = griddata(
            (strikes, expiries),
            volatilities,
            (grid_x_mesh, grid_y_mesh),
            method="linear"
        )
        grid_z = np.where(np.isnan(grid_z), grid_z_linear, grid_z)

    # Render 3D Surface with Plotly
    fig = go.Figure(
        data=[
            go.Surface(
                x=grid_x_mesh,
                y=grid_y_mesh,
                z=grid_z,
                colorscale="Viridis",
                colorbar=dict(title="Implied Volatility"),
            )
        ]
    )

    fig.update_layout(
        title=f"SVI Implied Volatility Surface: {ticker_symbol}",
        scene=dict(
            xaxis_title="Strike Price ($)",
            yaxis_title="Time to Expiration (Years)",
            zaxis_title="Implied Volatility (SVI Fitted)",
        ),
        autosize=True,
        width=1000,
        height=700,
    )
    
    # Save a static HTML fallback file and open in browser
    fig.write_html("vol_surface.html", auto_open=True)
    print("Surface rendered successfully! Saved to 'vol_surface.html'.")


if __name__ == "__main__":
    ticker = "SPY"
    df_surface, spot = fetch_and_calibrate_surface(ticker)
    print(f"Calibration Complete. Rendered {len(df_surface)} fitted surface grid points.")
    plot_3d_surface(df_surface, ticker)