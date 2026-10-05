import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from statsmodels.tsa.seasonal import seasonal_decompose
from scipy.stats import linregress


# ============================================================
# PRACTICAL WORK 22
# Time Series
# Student: Artem Oliinyk
# Group: IT-41
# Variant: 1
# City: Kyiv
# ============================================================

VARIANT = 1
CITY = "Kyiv"

base_temp = 9.5
amplitude = 14
trend_per_year = 0.04
noise_scale = 1.0


# ============================================================
# TASK 1. CREATE TIME SERIES
# ============================================================

np.random.seed(VARIANT)

n_years = 10

dates = pd.date_range(
    start="2015-01-01",
    periods=n_years * 12,
    freq="MS"
)

month = dates.month

years_elapsed = (
    (dates.year - dates.year[0])
    + (dates.month - 1) / 12
)

seasonal = amplitude * np.cos(
    (month - 7) / 12 * 2 * np.pi
)

trend = trend_per_year * years_elapsed

noise = np.random.normal(
    0,
    noise_scale,
    len(dates)
)

temp = np.round(
    base_temp + trend + seasonal + noise,
    1
)

climate_ts = pd.Series(
    temp,
    index=dates,
    name="temperature"
)


print("=" * 70)
print("PRACTICAL WORK 22")
print("Student: Artem Oliinyk")
print("Group: IT-41")
print("Variant: 1")
print("City: Kyiv")
print("=" * 70)

print("\nTASK 1. TIME SERIES")
print("-" * 70)

print(climate_ts.head(12))

print("\nNumber of observations:", len(climate_ts))

print(
    "\nThe time series contains 120 monthly observations "
    "for the period 2015-2024."
)

print(
    "The graph shows a strong annual seasonal cycle. "
    "There is also a small long-term warming trend."
)


# Graph 1

fig, ax = plt.subplots(figsize=(11, 5))

ax.plot(
    climate_ts.index,
    climate_ts.values
)

ax.set_xlabel("Date")
ax.set_ylabel("Temperature, C")
ax.set_title(
    "Monthly temperature in Kyiv, 2015-2024"
)

ax.grid(True)

plt.tight_layout()
plt.show()


# ============================================================
# TASK 2. MOVING AVERAGE
# ============================================================

print("\nTASK 2. MOVING AVERAGE")
print("-" * 70)

ma3 = climate_ts.rolling(
    window=3,
    center=True
).mean()

ma12_center = climate_ts.rolling(
    window=12,
    center=True
).mean()

ma12_trailing = climate_ts.rolling(
    window=12
).mean()


fig, ax = plt.subplots(figsize=(11, 5))

ax.plot(
    climate_ts.index,
    climate_ts.values,
    alpha=0.35,
    label="Original"
)

ax.plot(
    ma3.index,
    ma3.values,
    label="MA 3 centered"
)

ax.plot(
    ma12_center.index,
    ma12_center.values,
    label="MA 12 centered"
)

ax.plot(
    ma12_trailing.index,
    ma12_trailing.values,
    label="MA 12 trailing"
)

ax.set_xlabel("Date")
ax.set_ylabel("Temperature, C")
ax.set_title("Moving averages")

ax.legend()
ax.grid(True)

plt.tight_layout()
plt.show()


print(
    "The 3-month moving average reduces short-term noise, "
    "but the annual seasonal cycle is still visible."
)

print(
    "The 12-month moving average removes most of the annual "
    "seasonality because the window is equal to one full "
    "seasonal period."
)

print(
    "The trailing 12-month moving average has a visible lag "
    "because each value uses the current and previous months."
)

print(
    "The centered moving average is positioned near the "
    "center of the observations used in its calculation, "
    "so it represents the underlying trend more accurately."
)


# ============================================================
# TASK 3. SEASONAL DECOMPOSITION
# ============================================================

print("\nTASK 3. SEASONAL DECOMPOSITION")
print("-" * 70)

decomposition = seasonal_decompose(
    climate_ts,
    model="additive",
    period=12
)

fig = decomposition.plot()
fig.set_size_inches(10, 8)

plt.tight_layout()
plt.show()


trend_component = decomposition.trend
seasonal_component = decomposition.seasonal
resid_component = decomposition.resid


print("\nFirst 12 seasonal values:")

print(
    seasonal_component.head(12).round(2)
)


resid_std = resid_component.dropna().std()

print(
    f"\nResidual standard deviation: "
    f"{resid_std:.4f} C"
)


# Find warmest and coldest month

seasonal_by_month = seasonal_component.groupby(
    seasonal_component.index.month
).mean()

warmest_month = seasonal_by_month.idxmax()
coldest_month = seasonal_by_month.idxmin()

month_names = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December"
}

print(
    f"Warmest seasonal month: "
    f"{month_names[warmest_month]}"
)

print(
    f"Coldest seasonal month: "
    f"{month_names[coldest_month]}"
)

print(
    "\nThe estimated trend changes slowly over time "
    "and generally follows the warming trend included "
    "in the generated data."
)

print(
    "The seasonal component shows the repeating annual "
    "temperature cycle with the highest values around July."
)

print(
    f"The residual standard deviation is {resid_std:.4f} C. "
    f"The original noise scale was {noise_scale:.1f} C."
)


# ============================================================
# TASK 4. FORECAST
# ============================================================

print("\nTASK 4. FORECAST")
print("-" * 70)

trend_clean = decomposition.trend.dropna()

x = np.arange(len(trend_clean))

fit = linregress(
    x,
    trend_clean.values
)

print(
    f"Trend slope: {fit.slope:.6f} C/month"
)

print(
    f"Trend slope per year: "
    f"{fit.slope * 12:.6f} C/year"
)

print(
    f"p-value: {fit.pvalue:.8f}"
)

print(
    f"Standard error: {fit.stderr:.8f}"
)


# Forecast 12 months

n_ahead = 12

x_future = np.arange(
    len(trend_clean),
    len(trend_clean) + n_ahead
)

trend_forecast = (
    fit.intercept
    + fit.slope * x_future
)

future_dates = pd.date_range(
    climate_ts.index[-1]
    + pd.offsets.MonthBegin(1),
    periods=n_ahead,
    freq="MS"
)

seasonal_forecast = seasonal_by_month.reindex(
    future_dates.month
).values

forecast = pd.Series(
    trend_forecast + seasonal_forecast,
    index=future_dates,
    name="forecast"
)


print("\nForecast for next 12 months:")
print(forecast.round(2))


# Forecast graph

fig, ax = plt.subplots(figsize=(11, 5))

ax.plot(
    climate_ts.index,
    climate_ts.values,
    label="Historical data"
)

ax.plot(
    forecast.index,
    forecast.values,
    marker="o",
    label="Forecast"
)

ax.set_xlabel("Date")
ax.set_ylabel("Temperature, C")

ax.set_title(
    "Kyiv temperature: historical data and forecast"
)

ax.legend()
ax.grid(True)

plt.tight_layout()
plt.show()


print(
    "\nForecast warning:"
)

print(
    "This forecast is based on extending the historical "
    "linear trend and repeating the average seasonal pattern. "
    "It should not be interpreted as an exact weather forecast."
)

print(
    "Real temperatures may be affected by unusual weather, "
    "climate variability and changes in the long-term trend "
    "that are not represented in this simple model."
)


# ============================================================
# TASK 5. TREND SIGNIFICANCE
# ============================================================

print("\nTASK 5. TREND SIGNIFICANCE")
print("-" * 70)

alpha = 0.05

ci_low = fit.slope - 1.96 * fit.stderr
ci_high = fit.slope + 1.96 * fit.stderr

print("H0: true trend slope = 0")
print("H1: true trend slope != 0")

print(
    f"\nSlope = {fit.slope:.8f} C/month"
)

print(
    f"p-value = {fit.pvalue:.8f}"
)

print(
    f"95% CI: [{ci_low:.8f}; {ci_high:.8f}] C/month"
)


if fit.pvalue < alpha:
    print(
        "\nResult: reject H0 at alpha = 0.05."
    )

    print(
        "There is statistical evidence of a non-zero "
        "temperature trend."
    )

else:
    print(
        "\nResult: do not reject H0 at alpha = 0.05."
    )

    print(
        "There is not enough statistical evidence "
        "of a non-zero temperature trend."
    )


# ============================================================
# SHORT WINDOW: LAST 3 YEARS
# ============================================================

last_3_years = climate_ts.iloc[-36:]

decomp_short = seasonal_decompose(
    last_3_years,
    model="additive",
    period=12
)

short_trend = decomp_short.trend.dropna()

x_short = np.arange(len(short_trend))

fit_short = linregress(
    x_short,
    short_trend.values
)


print("\nLast 3 years analysis:")
print(
    f"Slope = {fit_short.slope:.8f} C/month"
)

print(
    f"Slope per year = "
    f"{fit_short.slope * 12:.6f} C/year"
)

print(
    f"p-value = {fit_short.pvalue:.8f}"
)


print(
    "\nA trend estimated from only the last three years "
    "can differ noticeably from the ten-year estimate."
)

print(
    "On a short time interval random temperature fluctuations "
    "can look like a trend more easily, so the estimate is "
    "less reliable."
)


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("FINAL SUMMARY")
print("=" * 70)

print("Student: Artem Oliinyk")
print("Group: IT-41")
print("Variant: 1")
print("City: Kyiv")

print(
    f"\nEstimated trend: "
    f"{fit.slope * 12:.6f} C/year"
)

print(
    f"p-value: {fit.pvalue:.8f}"
)

print(
    f"Residual standard deviation: "
    f"{resid_std:.4f} C"
)

print(
    f"Warmest month: "
    f"{month_names[warmest_month]}"
)

print(
    f"Coldest month: "
    f"{month_names[coldest_month]}"
)

if fit.pvalue < 0.05:
    print(
        "Conclusion: the trend is statistically significant "
        "at alpha = 0.05."
    )
else:
    print(
        "Conclusion: the trend is not statistically significant "
        "at alpha = 0.05."
    )