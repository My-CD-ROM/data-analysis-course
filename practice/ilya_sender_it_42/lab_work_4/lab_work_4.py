import numpy as np
import pandas as pd

# Завдання 1. Побудова брудного набору

orders = pd.DataFrame([
    {"id": 1, "місто": "Суми",   "товар": "Товар 9", "ціна": 730,       "кількість": 2},
    {"id": 2, "місто": " Суми ", "товар": "Товар 9", "ціна": "730 грн", "кількість": 3},
    {"id": 3, "місто": "СУМИ",   "товар": "Товар 9", "ціна": 750,       "кількість": np.nan},
    {"id": 4, "місто": "Суми",   "товар": "Товар 9", "ціна": "730 грн", "кількість": 1},
    {"id": 5, "місто": "Суми",   "товар": "Товар 9", "ціна": 5840,      "кількість": 2},
    {"id": 6, "місто": "Суми",   "товар": "Товар 9", "ціна": 720,       "кількість": np.nan},
    {"id": 7, "місто": "Суми",   "товар": "Товар 9", "ціна": 740,       "кількість": 2},
    {"id": 7, "місто": "Суми",   "товар": "Товар 9", "ціна": 740,       "кількість": 2}
])

print("Брудний набір:")
print(orders)


# Завдання 2. Пропуски
print(orders.isna().sum())
median_quantity = orders["кількість"].median()
print("\nМедіана кількості:", median_quantity)
orders["кількість"] = orders["кількість"].fillna(median_quantity)
print("\nПісля заповнення пропусків:")
print(orders)

# Завдання 3. Дублікати
print(orders[orders.duplicated()])
print(orders.duplicated().sum())
print(orders.duplicated(subset=["місто", "товар"]).sum())
#2
orders = orders.drop_duplicates()
print(len(orders))


# Завдання 4. Типи даних і категорії

orders["ціна"] = (orders["ціна"].astype(str).str.replace(" грн", "", regex=False).astype(float))

print("\nТип ціни після очищення:")
print(orders["ціна"].dtype)

orders["місто"] = orders["місто"].str.strip().str.lower()

orders["місто"] = orders["місто"].replace({"суми": "Суми"})

print("\nУнікальні назви міст:")
print(orders["місто"].unique())
print(orders)

# Завдання 5. Викиди

q1 = orders["ціна"].quantile(0.25)
q3 = orders["ціна"].quantile(0.75)

iqr = q3 - q1

lower = q1 - 1.5 * iqr
upper = q3 + 1.5 * iqr

print("\nQ1:", q1)
print("Q3:", q3)
print("IQR:", iqr)
print("Нижня межа:", lower)
print("Верхня межа:", upper)

outliers = orders[(orders["ціна"] < lower) | (orders["ціна"] > upper)]

print("\nВикиди:")
print(outliers)
print("\n5840 / 730 =", 5840 / 730)
orders.loc[orders["ціна"] == 5840, "ціна"] = 730
print(orders)
