# Active Duration Forecasting with ARMA-GARCH and Monte Carlo Simulation

This project applies ARMA-GARCH modeling and Monte Carlo simulation to forecast future values of active duration in a fixed income portfolio. The goal is to assess the probability of breaching Investment Policy Statement (IPS) limits on duration risk over a 30-day horizon.

## Objectives

- Test the stationarity of the active duration series
- Fit an ARMA(1,1) model to capture the mean structure
- Fit a GARCH(1,1) model to capture conditional volatility
- Forecast mean and variance of active duration over a 30-day horizon
- Use Monte Carlo simulation to estimate the distribution of future outcomes
- Identify whether IPS thresholds (±1) may be breached under 99% confidence level

## Methodology

1. **Data Loading**  
   Active duration data is loaded from an Excel file containing historical duration values and dates.

2. **Stationarity Testing**  
   The Augmented Dickey-Fuller (ADF) test is used to assess whether the series is stationary.

3. **Model Estimation**  
   - An ARMA(1,1) model is fitted to the series to estimate expected future returns.
   - Residuals from the ARMA model are used to fit a GARCH(1,1) model for volatility clustering.

4. **Forecasting**  
   - A 30-day ahead forecast is generated for both the conditional mean and volatility.
   - A 99% confidence interval is constructed using the forecasted standard deviation.

5. **Monte Carlo Simulation**  
   - 1000 simulation paths are generated by combining forecasted mean and random shocks.
   - Simulated paths illustrate a range of possible active duration outcomes.

6. **Risk Assessment**  
   - Forecast results are compared against ±1 duration unit IPS thresholds.
   - The code flags any scenario where the upper or lower forecast bounds exceed IPS limits.

7. **Visualization**  
   - A comprehensive plot displays historical data, simulated paths, mean forecast, and IPS bands.

## Tools Used

- Python 3.x
- pandas, numpy
- statsmodels (for ARMA)
- arch (for GARCH modeling)
- matplotlib (for visualization)

## Key Takeaways

- Combined time series modeling and simulation to analyze fixed income duration risk
- Demonstrated the use of ARMA-GARCH for risk forecasting under uncertainty
- Visualized confidence bands and scenario risk relative to IPS policy constraints

## Notes

- This analysis is for illustrative academic purposes using sample or internal data
- In real-world application, model diagnostics and tuning should be further validated
