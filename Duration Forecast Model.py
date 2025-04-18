import pandas as pd
import numpy as np
from arch import arch_model
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt

# Step 1: Load Data from Excel
file_path = 'active_duration_data.xlsx'  # Replace with your file path
data = pd.read_excel(file_path)

# Assume the column with data is named 'Active Duration' and dates are in 'Date' column
y = data['Active Duration']
dates = pd.to_datetime(data['Date'])  # Convert dates to datetime format for plotting

# Check for Stationarity
from statsmodels.tsa.stattools import adfuller

# Perform ADF Test
result = adfuller(y)
print(f'ADF Statistic: {result[0]}')
print(f'p-value: {result[1]}')

if result[1] <= 0.05:
    print("The data is stationary (p-value ≤ 0.05).")
else:
    print("The data is non-stationary (p-value > 0.05). Consider differencing the data.")

# Step 2: Fit ARMA Model (1,1)
arma_model = ARIMA(y, order=(1, 0, 1))  # ARMA(1,1)
arma_result = arma_model.fit()

# Step 3: Fit GARCH Model (1,1)
residuals = arma_result.resid
garch_model = arch_model(residuals, vol='Garch', p=1, q=1)
garch_result = garch_model.fit()

# Step 4: Forecast for One Week (30 days)
forecast_horizon = 30
arma_forecast = arma_result.get_forecast(steps=forecast_horizon)
garch_forecast = garch_result.forecast(start=0, horizon=forecast_horizon)

# Extract forecasted mean and standard deviation
forecast_mean = arma_forecast.predicted_mean
forecast_std = np.sqrt(garch_forecast.variance.values[-1, :])

# Step 5: Simulate 1000 Paths for Monte Carlo Simulation
num_simulations = 1000
simulated_paths = np.zeros((forecast_horizon, num_simulations))

for i in range(num_simulations):
    shocks = np.random.normal(0, forecast_std, forecast_horizon)
    simulated_paths[:, i] = forecast_mean + shocks

# Step 6: Create Confidence Interval (95%)
#z_score = 1.96  # For 95% confidence interval
#upper_bound = forecast_mean + z_score * forecast_std
#lower_bound = forecast_mean - z_score * forecast_std

# Step 6: Create Confidence Interval (99%)
z_score = 2.576  # For 99% confidence interval
upper_bound = forecast_mean + z_score * forecast_std
lower_bound = forecast_mean - z_score * forecast_std

# Step 7: Extend Dates for Forecast
last_date = dates.iloc[-1]
forecast_dates = pd.date_range(start=last_date, periods=forecast_horizon + 1, freq='D')[1:]

# Step 8: Plot Results
plt.figure(figsize=(12, 6))
plt.plot(dates, y, color='purple', linewidth=2, label='Historical Active Duration')  # Plot full historical data

# Plot simulated paths
for i in range(num_simulations):
    plt.plot(forecast_dates, simulated_paths[:, i], color='orange', alpha=0.05)  # Faint lines for each simulation

# Plot forecasted mean and confidence intervals
plt.plot(forecast_dates, forecast_mean, color='green', linewidth=2, label='Forecasted Mean (1-Week)')
plt.fill_between(forecast_dates, lower_bound, upper_bound, color='blue', alpha=0.2, label='99% Confidence Interval')
plt.axhline(y=1, color='r', linestyle='--', label='+1 IPS Threshold')
plt.axhline(y=-1, color='b', linestyle='--', label='-1 IPS Threshold')
plt.title('Active Duration with 1-Month Forward Forecast (ARMA-GARCH Model)')
plt.xlabel('Date')
plt.ylabel('Active Duration')
plt.xticks(rotation=45)
plt.legend()
plt.show()

# Step 9: IPS Breach Check
breach_upper = (upper_bound > 1).any()
breach_lower = (lower_bound < -1).any()

if breach_upper or breach_lower:
    print("Warning: There is a risk of breaching the IPS limits in the forecast period.")
else:
    print("The forecast suggests minimal risk of breaching the IPS limits in the next week (99% confidence).")
