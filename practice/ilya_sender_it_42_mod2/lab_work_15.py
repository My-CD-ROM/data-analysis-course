import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency, chisquare

# Варіант 9 — Суми
np.random.seed(42)

base_temp = 7.5
amplitude = 14
city = "Суми"

def season(month):
    if month in (12, 1, 2):
        return "зима"
    if month in (3, 4, 5):
        return "весна"
    if month in (6, 7, 8):
        return "літо"
    return "осінь"

rows = []

for year in [2021, 2022, 2023, 2024]:
    for month in range(1, 13):
        seasonal = amplitude * np.cos((month - 7) / 12 * 2 * np.pi)
        noise = np.random.normal(0, 1.0)
        temp = round(base_temp + seasonal + noise, 1)

        diff = temp - base_temp

        if diff < -3:
            norm_cat = "холодніше"
        elif diff > 3:
            norm_cat = "тепліше"
        else:
            norm_cat = "звичайно"

        rows.append({
            "місто": city,
            "рік": year,
            "місяць": month,
            "температура": temp,
            "сезон": season(month),
            "відхилення_від_норми": norm_cat
        })

climate = pd.DataFrame(rows)

# Завдання 1. Таблиця спряженості

table = pd.crosstab(
    climate["сезон"],
    climate["відхилення_від_норми"]
).reindex(["зима", "весна", "літо", "осінь"])

print("Фактична таблиця:")
print(table)

table_norm = pd.crosstab(
    climate["сезон"],
    climate["відхилення_від_норми"],
    normalize="index"
).reindex(["зима", "весна", "літо", "осінь"])

print("\nНормована таблиця:")
print(table_norm)

# Завдання 2. Критерій незалежності

chi2, p_value, dof, expected = chi2_contingency(table)

expected_df = pd.DataFrame(
    expected,
    index=table.index,
    columns=table.columns
)

print("\nЗавдання 2")
print("chi2 =", chi2)
print("p-value =", p_value)
print("dof =", dof)
print("Очікувані частоти:")
print(expected_df)

# Завдання 3. Перевірка умови застосовності

print("\nЗавдання 3")
print("Усі expected >= 5:", (expected >= 5).all())

# Об'єднуємо "холодніше" та "звичайно"
table_combined = pd.DataFrame({
    "не тепліше": table["холодніше"] + table["звичайно"],
    "тепліше": table["тепліше"]
})

chi2_comb, p_comb, dof_comb, expected_comb = chi2_contingency(
    table_combined
)

print("\nТаблиця після об'єднання:")
print(table_combined)

print("chi2 =", chi2_comb)
print("p-value =", p_comb)
print("dof =", dof_comb)

print("Очікувані частоти після об'єднання:")
print(pd.DataFrame(
    expected_comb,
    index=table_combined.index,
    columns=table_combined.columns
))

# Завдання 4. Критерій узгодженості для сезонів

season_counts = climate["сезон"].value_counts().reindex(
    ["зима", "весна", "літо", "осінь"]
)

expected_seasons = [12, 12, 12, 12]

season_test = chisquare(
    f_obs=season_counts,
    f_exp=expected_seasons
)

print("\nЗавдання 4")
print("Частоти сезонів:")
print(season_counts)
print("chi2 =", season_test.statistic)
print("p-value =", season_test.pvalue)

# Завдання 5. Власна заявлена пропорція

# H0: холодніше = 20%, звичайно = 60%, тепліше = 20%
observed = climate["відхилення_від_норми"].value_counts().reindex(
    ["звичайно", "тепліше", "холодніше"]
)

n = len(climate)
expected_custom = [0.60 * n, 0.20 * n, 0.20 * n]

custom_test = chisquare(
    f_obs=observed,
    f_exp=expected_custom
)

print("\nЗавдання 5")
print("Фактичні частоти:")
print(observed)
print("Очікувані частоти:", expected_custom)
print("chi2 =", custom_test.statistic)
print("p-value =", custom_test.pvalue)
