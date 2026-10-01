import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

variant_number = 1
july_temp = 21.0

np.random.seed(variant_number)
daily_temps = np.random.normal(loc=july_temp, scale=2.5, size=30)

print("Масив daily_temps:", daily_temps)
print("Вибіркове середнє:", daily_temps.mean())
print("Вибіркове стандартне відхилення:", daily_temps.std())

mean, std = daily_temps.mean(), daily_temps.std()
dist = stats.norm(loc=mean, scale=std)

x = np.linspace(daily_temps.min() - 3, daily_temps.max() + 3, 200)

plt.figure(figsize=(8, 5))
plt.hist(daily_temps, bins=7, density=True, edgecolor="white", alpha=0.7, color="skyblue")
plt.plot(x, dist.pdf(x), color="crimson", linewidth=2, label="Теоретична PDF")
plt.title(f"Варіант {variant_number} (Київ) — Розподіл липневих температур")
plt.xlabel("Температура (°C)")
plt.ylabel("Густина ймовірності")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.5)
plt.show()

p_within_1std = dist.cdf(mean + std) - dist.cdf(mean - std)
print(f"Ймовірність P(mean - std <= X <= mean + std): {p_within_1std:.4f}")

percentile_95 = dist.ppf(0.95)
print(f"95-й процентиль: {percentile_95:.2f} °C")