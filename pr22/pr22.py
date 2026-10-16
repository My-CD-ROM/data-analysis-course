import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from scipy.stats import linress

# ==========================================
# ГЕНЕРАЦІЯ ДАНИХ (ВАРІАНТ 1 — КИЇВ)
# ==========================================
np.random.seed(1)  # Номер варіанта: 1

base_temp = 9.5          # Середньорічна температура, °C
amplitude = 14.0         # Сезонна амплітуда, °C
trend_per_year = 0.04    # Тренд потепління, °C/рік
noise_scale = 1.0        # σ шуму, °C
city = "Київ"

n_years = 10
dates = pd.date_range(start="2015-01-01", periods=n_years * 12, freq="MS")
month = dates.month
years_elapsed = (dates.year - dates.year[0]) + (dates.month - 1) / 12

seasonal = amplitude * np.cos((month - 7) / 12 * 2 * np.pi)
trend = trend_per_year * years_elapsed
noise = np.random.normal(0, noise_scale, len(dates))

temp = np.round(base_temp + trend + seasonal + noise, 1)
climate_ts = pd.Series(temp, index=dates, name="температура")

# ==========================================
# ЗАВДАННЯ 1: Візуалізація первинного ряду
# ==========================================
plt.figure(figsize=(11, 4))
plt.plot(climate_ts.index, climate_ts.values, label="Температура (°C)", color="tab:blue")
plt.title(f"10-річний кліматичний часовий ряд (Варіант 1 — {city})")
plt.xlabel("Дата")
plt.ylabel("Температура, °C")
plt.grid(True, linestyle=":", alpha=0.6)
plt.legend()
plt.tight_layout()
plt.show()

# ==========================================
# ЗАВДАННЯ 2: Ковзне середнє (згладжування та лаг)
# ==========================================
ma3_center = climate_ts.rolling(window=3, center=True).mean()
ma12_center = climate_ts.rolling(window=12, center=True).mean()
ma12_trailing = climate_ts.rolling(window=12, center=False).mean()

fig, ax = plt.subplots(figsize=(11, 5))
ax.plot(climate_ts.index, climate_ts.values, alpha=0.35, color="gray", label="Оригінальний ряд")
ax.plot(climate_ts.index, ma3_center.values, label="Центроване MA (вікно = 3)", color="tab:orange")
ax.plot(climate_ts.index, ma12_center.values, label="Центроване MA (вікно = 12)", color="tab:green", linewidth=2)
ax.plot(climate_ts.index, ma12_trailing.values, label="Трейлінгове MA (вікно = 12)", color="tab:red", linestyle="--")
ax.set_title("Порівняння варіантів ковзного середнього")
ax.set_xlabel("Дата")
ax.set_ylabel("Температура, °C")
ax.grid(True, linestyle=":", alpha=0.6)
ax.legend()
plt.tight_layout()
plt.show()

# ==========================================
# ЗАВДАННЯ 3: Декомпозиція seasonal_decompose
# ==========================================
decomp = seasonal_decompose(climate_ts, model="additive", period=12)

fig = decomp.plot()
fig.set_size_inches(10, 7)
plt.tight_layout()
plt.show()

std_resid = decomp.resid.dropna().std()
print("=== ЗАВДАННЯ 3: РЕЗУЛЬТАТИ ДЕКОМПОЗИЦІЇ ===")
print(f"Стандартне відхилення залишку (resid): {std_resid:.2f}°C (закладений noise_scale = {noise_scale}°C)")

# ==========================================
# ЗАВДАННЯ 4: Прогноз на 12 місяців уперед
# ==========================================
trend_clean = decomp.trend.dropna()
x_trend = np.arange(len(trend_clean))
fit = linregress(x_trend, trend_clean.values)

n_ahead = 12
x_future = np.arange(len(trend_clean), len(trend_clean) + n_ahead)
trend_forecast = fit.intercept + fit.slope * x_future

seasonal_by_month = decomp.seasonal.groupby(decomp.seasonal.index.month).mean()
future_dates = pd.date_range(climate_ts.index[-1] + pd.offsets.MonthBegin(1), periods=n_ahead, freq="MS")
seasonal_forecast = seasonal_by_month.reindex(future_dates.month).values

forecast = pd.Series(trend_forecast + seasonal_forecast, index=future_dates, name="прогноз")

print("\n=== ЗАВДАННЯ 4: ПРОГНОЗ НА 12 МІСЯЦІВ УПЕРЕД ===")
print(forecast.round(2))

plt.figure(figsize=(11, 4.5))
plt.plot(climate_ts.index, climate_ts.values, label="Історичні дані (2015–2024)", color="tab:blue")
plt.plot(forecast.index, forecast.values, label="Прогноз на 2025 рік", color="tab:red", linestyle="--", marker="o")
plt.title("Прогноз середньомісячної температури на 12 місяців")
plt.xlabel("Дата")
plt.ylabel("Температура, °C")
plt.grid(True, linestyle=":", alpha=0.6)
plt.legend()
plt.tight_layout()
plt.show()

# ==========================================
# ЗАВДАННЯ 5: Оцінка статистичної значущості тренду
# ==========================================
slope_monthly = fit.slope
slope_annual = slope_monthly * 12
p_val = fit.pvalue
stderr_monthly = fit.stderr
stderr_annual = stderr_monthly * 12

ci_lower = slope_annual - 1.96 * stderr_annual
ci_upper = slope_annual + 1.96 * stderr_annual

print("\n=== ЗАВДАННЯ 5: СТАТИСТИЧНИЙ АНАЛІЗ ТРЕНДУ ===")
print(f"Оцінений річний нахил тренду: {slope_annual:.4f} °C/рік (істинний: {trend_per_year} °C/рік)")
print(f"p-value нахилу: {p_val:.2e}")
print(f"95% довірчий інтервал для річного тренду: [{ci_lower:.4f}, {ci_upper:.4f}] °C/рік")

# Аналіз на коротку підвибірку (останні 30 місяців)
trend_short = decomp.trend.dropna().tail(30)
x_short = np.arange(len(trend_short))
fit_short = linregress(x_short, trend_short.values)

print(f"\nКоротке вікно (останні 2.5 роки / 30 місяців):")
print(f"Оцінений річний нахил: {fit_short.slope * 12:.4f} °C/рік")
print(f"p-value на короткому вікні: {fit_short.pvalue:.4e}")