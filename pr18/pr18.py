import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
import matplotlib.pyplot as plt
import scipy.stats as stats

np.random.seed(42)
city = "Київ"
mean_temp = 9.5
amplitude = 14
hum_base = 74

rows = []
for month in range(1, 13):
    temp = mean_temp + amplitude * np.cos((month - 7) / 12 * 2 * np.pi) + np.random.normal(0, 1.0)
    humidity = hum_base + np.random.normal(0, 5.0)
    if temp < 8:
        opal_days = 30
    elif temp < 12:
        opal_days = 15
    else:
        opal_days = 0

    cost = (
        200
        - 9.0 * temp
        + 0.6 * humidity
        + 2.5 * opal_days
        + np.random.normal(0, 15)
    )
    rows.append({
        "місто": city, "місяць": month,
        "температура": round(temp, 1),
        "вологість": round(humidity, 1),
        "опалювальні_дні": opal_days,
        "витрати_на_опалення": round(cost, 1),
    })
heating = pd.DataFrame(rows)

# Завдання 1
X1 = sm.add_constant(heating[["температура", "вологість"]])
y = heating["витрати_на_опалення"]
model1 = sm.OLS(y, X1).fit()

print("=== ЗАВДАННЯ 1: МОДЕЛЬ З ДВОМА ПРЕДИКТОРAМИ ===")
print(model1.summary())

# Завдання 2
print("\n=== ЗАВДАННЯ 2: ІНТЕРПРЕТАЦІЯ КОЕФІЦІЄНТІВ ===")
print(f"Intercept: {model1.params['const']:.4f}, p-value: {model1.pvalues['const']:.4e}")
print(f"Температура: {model1.params['температура']:.4f}, p-value: {model1.pvalues['температура']:.4e}")
print(f"Вологість: {model1.params['вологість']:.4f}, p-value: {model1.pvalues['вологість']:.4e}")

# Завдання 3
print("\n=== ЗАВДАННЯ 3: VIF ДЛЯ МОДЕЛІ 1 ===")
for i, col in enumerate(X1.columns):
    if col == "const":
        continue
    vif = variance_inflation_factor(X1.values, i)
    print(f"{col}: VIF = {vif:.2f}")

# Завдання 4
X2 = sm.add_constant(heating[["температура", "вологість", "опалювальні_дні"]])
model2 = sm.OLS(y, X2).fit()

print("\n=== ЗАВДАННЯ 4: ПОРІВНЯННЯ МОДЕЛЕЙ (2 vs 3 ПРЕДИКТОРЫ) ===")
print(f"Модель 1 (2 предиктори): R² = {model1.rsquared:.4f}, Adj. R² = {model1.rsquared_adj:.4f}")
print(f"Модель 2 (3 предиктори): R² = {model2.rsquared:.4f}, Adj. R² = {model2.rsquared_adj:.4f}")

print("\nVIF для Моделі 2:")
for i, col in enumerate(X2.columns):
    if col == "const":
        continue
    vif = variance_inflation_factor(X2.values, i)
    print(f"{col}: VIF = {vif:.2f}")

# Завдання 5
fitted = model1.fittedvalues
residuals = model1.resid

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

ax1.scatter(fitted, residuals, color="blue")
ax1.axhline(0, color="red", linestyle="--")
ax1.set_xlabel("Передбачені витрати")
ax1.set_ylabel("Залишок")
ax1.set_title("Графік залишків проти передбачених значень")
ax1.grid(True, linestyle="--", alpha=0.6)

stats.probplot(residuals, dist="norm", plot=ax2)
ax2.set_title("QQ-plot залишків")
ax2.grid(True, linestyle="--", alpha=0.6)

plt.tight_layout()
plt.show()

shapiro_stat, shapiro_p = stats.shapiro(residuals)
print("\n=== ЗАВДАННЯ 5: ДІАГНОСТИКА ЗАЛИШКІВ ===")
print(f"Критерій Шапіро-Вілка: W = {shapiro_stat:.4f}, p-value = {shapiro_p:.4f}")

# Завдання 6
X_simple = sm.add_constant(heating[["температура"]])
model_simple = sm.OLS(y, X_simple).fit()

print("\n=== ЗАВДАННЯ 6: ПОРІВНЯННЯ З ПРОСТОЮ РЕГРЕСІЄЮ ===")
print(f"Проста регресія (лише температура): R² = {model_simple.rsquared:.4f}, Adj. R² = {model_simple.rsquared_adj:.4f}")
print(f"Множинна регресія (температура + вологість): R² = {model1.rsquared:.4f}, Adj. R² = {model1.rsquared_adj:.4f}")