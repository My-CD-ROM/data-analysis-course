import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# Варіант 9 — Суми

# Завдання 1. Побудова вибірки
np.random.seed(9)

daily_temps = np.random.normal(
    loc=20,
    scale=2.5,
    size=30
)

print("Вибірка:")
print(daily_temps)

print("\nСереднє:", daily_temps.mean())
print("Стандартне відхилення:", daily_temps.std())


# Завдання 2. Параметри нормального розподілу
mean = daily_temps.mean()
std = daily_temps.std()

dist = stats.norm(
    loc=mean,
    scale=std
)

print("\nПараметри нормального розподілу:")
print("mean =", mean)
print("std =", std)


# Завдання 3. Гістограма + PDF
x = np.linspace(
    daily_temps.min() - 2,
    daily_temps.max() + 2,
    200
)

plt.figure(figsize=(9, 5))

plt.hist(
    daily_temps,
    bins=8,
    density=True,
    edgecolor="white",
    alpha=0.7,
    label="Денні температури"
)

plt.plot(
    x,
    dist.pdf(x),
    linewidth=2,
    label="Теоретична pdf-крива"
)

plt.xlabel("Температура, °C")
plt.ylabel("Густина")
plt.title("Розподіл денних температур у Сумах")
plt.legend()
plt.show()


# Завдання 4. Ймовірність у межах ±1 стандартного відхилення
lower = mean - std
upper = mean + std

p = dist.cdf(upper) - dist.cdf(lower)

print("\nЗавдання 4:")
print("Нижня межа:", lower)
print("Верхня межа:", upper)
print("Ймовірність:", p)
print("Ймовірність у %:", p * 100)


# Завдання 5. 95-й процентиль
percentile_95 = dist.ppf(0.95)

print("\nЗавдання 5:")
print("95-й процентиль:", percentile_95, "°C")
