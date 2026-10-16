import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(1)
city = "Київ"
base_temp = 9.5
amplitude = 14
base_consumption = 5200
k = 55
noise_sd = 80

months = np.arange(1, 13)
temp = base_temp + amplitude * np.cos((months - 7) / 12 * 2 * np.pi)
temp = np.round(temp + np.random.normal(0, 0.5, size=12), 1)

consumption = base_consumption - k * (temp - base_temp) + np.random.normal(0, noise_sd, size=12)
consumption = np.round(consumption, 0)

city_data = pd.DataFrame({
    "місяць": months,
    "температура": temp,
    "споживання_МВтгод": consumption
})

# Завдання 2
b, a = np.polyfit(city_data["температура"], city_data["споживання_МВтгод"], 1)
city_data["передбачення"] = np.round(a + b * city_data["температура"], 1)

print("=== ЗАВДАННЯ 2: ПІДБІР МОДЕЛІ ===")
print(f"Отримана модель: споживання ≈ {a:.1f} + ({b:.1f}) * температура")

# Завдання 3
city_data["залишок"] = np.round(city_data["споживання_МВтгод"] - city_data["передбачення"], 1)

ss_res = (city_data["залишок"] ** 2).sum()
ss_tot = ((city_data["споживання_МВтгод"] - city_data["споживання_МВтгод"].mean()) ** 2).sum()
r_squared = 1 - ss_res / ss_tot

print("\n=== ЗАВДАННЯ 3: ТАБЛИЦЯ РЕЗУЛЬТАТІВ ТА R² ===")
print(city_data[["місяць", "температура", "споживання_МВтгод", "передбачення", "залишок"]])
print(f"\nR² (Коефіцієнт детермінації) = {r_squared:.4f}")

plt.figure(figsize=(10, 4))
plt.scatter(city_data["місяць"], city_data["залишок"], color="red", s=50)
plt.axhline(0, color="gray", linestyle="--")
plt.xticks(months)
plt.xlabel("Місяць")
plt.ylabel("Залишок (МВт·год)")
plt.title("Графік залишків за місяцями (Варіант 1 — Київ)")
plt.grid(True, linestyle=":", alpha=0.6)
plt.tight_layout()
plt.show()

# Завдання 4: Ручний розрахунок для верифікації
test_temp = city_data.loc[0, "температура"]
test_pred_code = city_data.loc[0, "передбачення"]
test_pred_manual = np.round(a + b * test_temp, 1)

print("\n=== ЗАВДАННЯ 4: ВЕРИФІКАЦІЯ КОДУ ===")
print(f"Місяць 1: темп = {test_temp}°C")
print(f"Передбачення коду: {test_pred_code}")
print(f"Ручний розрахунок (a + b*temp): {test_pred_manual}")