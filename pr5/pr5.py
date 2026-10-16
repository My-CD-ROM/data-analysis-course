import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

months = ["Січ", "Лют", "Бер", "Кві", "Тра", "Чер", "Лип", "Сер", "Вер", "Жов", "Лис", "Гру"]
data = [47, 44, 38, 43, 60, 78, 88, 70, 48, 41, 47, 50]
precip = pd.Series(data, index=months)

# 1. Варіаційний ряд
sorted_series = precip.sort_values()
print("Варіаційний ряд:", sorted_series.values)

# 2. Частотна таблиця (4 інтервали)
bins = [38, 50.5, 63.0, 75.5, 88.01]
labels = ["38.0-50.5", "50.5-63.0", "63.0-75.5", "75.5-88.0"]
cats = pd.cut(precip, bins=bins, labels=labels, right=False)

abs_freq = cats.value_counts().sort_index()
rel_freq = (abs_freq / len(precip) * 100).round(1)
cum_freq = abs_freq.cumsum()

freq_table = pd.DataFrame({
    "Інтервал (мм)": labels,
    "Абсолютна": abs_freq.values,
    "Відносна (%)": rel_freq.values,
    "Накопичена": cum_freq.values
})
print("\nЧастотна таблиця:\n", freq_table)

# 3. Міри положення та квантилі
print(f"\nСереднє: {precip.mean():.2f}")
print(f"Медіана: {precip.median():.2f}")
print(f"Мода: {precip.mode().tolist()}")
print(f"Q1: {precip.quantile(0.25):.2f}")
print(f"Q3: {precip.quantile(0.75):.2f}")

# 4. Побудова гістограм
fig, axes = plt.subplots(1, 3, figsize=(15, 4))

axes[0].hist(precip, bins=3, color='skyblue', edgecolor='black')
axes[0].set_title("3 інтервали (мала кількість)")

axes[1].hist(precip, bins=4, color='lightgreen', edgecolor='black')
axes[1].set_title("4 інтервали (оптимальна / Стерджес)")

axes[2].hist(precip, bins=10, color='salmon', edgecolor='black')
axes[2].set_title("10 інтервалів (надмірна подрібненість)")

for ax in axes:
    ax.set_xlabel("Опади (мм)")
    ax.set_ylabel("Частота")

plt.tight_layout()
plt.show()