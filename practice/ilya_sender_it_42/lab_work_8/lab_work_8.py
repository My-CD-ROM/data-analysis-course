import numpy as np
import pandas as pd

np.random.seed(42)

city = "Суми"
base_temp = 7.5
amplitude = 14

rows = []

for year in [2021, 2022, 2023, 2024]:
    for month in range(1, 13):
        seasonal = amplitude * np.cos((month - 7) / 12 * 2 * np.pi)
        noise = np.random.normal(0, 1.0)

        rows.append({
            "місто": city,
            "рік": year,
            "місяць": month,
            "температура": round(base_temp + seasonal + noise, 1)
        })

climate = pd.DataFrame(rows)

print("Варіант 9")
print("Місто:", city)
print("Середньорічна температура:", base_temp)
print("Сезонна амплітуда:", amplitude)

print("\nВихідний набір даних:")
print(climate)


print("\nЗавдання 1. groupby і agg за роками")

year_stats = climate.groupby("рік")["температура"].agg(
    ["mean", "min", "max"]
)

print(year_stats)

print("\nВисновок:")
print("Середні температури за роками коливаються.")
print("Для визначення стійкого тренду потрібно порівняти середні значення")
print("та врахувати випадкові відхилення, які були додані під час генерації.")


print("\nЗавдання 2. groupby і agg за місяцями")

month_stats = climate.groupby("місяць")["температура"].agg(
    ["mean", "std"]
)

print(month_stats)

max_std_month = month_stats["std"].idxmax()
max_std = month_stats["std"].max()

print("\nМісяць із найбільшим стандартним відхиленням:",
      max_std_month)

print("Стандартне відхилення:",
      round(max_std, 2))

print("\nВисновок:")
print("Найбільший розкид між роками може бути пов'язаний")
print("з випадковими коливаннями температури.")
print("Перехідні сезони також можуть мати більшу нестабільність.")


print("\nЗавдання 3. pivot_table")

pivot_table = climate.pivot_table(
    index="місяць",
    columns="рік",
    values="температура",
    aggfunc="mean"
)

print(pivot_table)

print("\nВисновок:")
print("Зведена таблиця зручніша для порівняння температури")
print("одного місяця між різними роками.")
print("Довгий формат зручніший для groupby, фільтрації")
print("та подальшої обробки даних.")


print("\nЗавдання 4. Похідні категорії і crosstab")

def get_season(month):
    if month in [12, 1, 2]:
        return "Зима"
    elif month in [3, 4, 5]:
        return "Весна"
    elif month in [6, 7, 8]:
        return "Літо"
    else:
        return "Осінь"


climate["сезон"] = climate["місяць"].apply(get_season)

climate["тепліше_за_середнє"] = (
    climate["температура"] > base_temp
)

print("Дані з новими стовпцями:")
print(climate)

cross_table = pd.crosstab(
    climate["сезон"],
    climate["тепліше_за_середнє"]
)

print("\nCrosstab:")
print(cross_table)

print("\nВисновок:")
print("Влітку більшість значень повинна бути в категорії")
print("'тепліше за середнє', а взимку — переважно нижче")
print("за середньорічну температуру.")


print("\nЗавдання 5. pivot() на своєму наборі")

pivot_result = climate.pivot(
    index="місяць",
    columns="рік",
    values="температура"
)

print(pivot_result)

print("\nВисновок:")
print("pivot() працює, тому що для кожної комбінації")
print("'місяць + рік' існує лише один рядок.")

print("У наборі 12 місяців × 4 роки = 48 рядків.")

print("Якби для одного місяця та року було кілька рядків,")
print("наприклад через кілька метеостанцій,")
print("pivot() завершився б помилкою через дублікати.")
print("У такому випадку потрібно використовувати pivot_table(),")
print("який може агрегувати кілька значень.")
