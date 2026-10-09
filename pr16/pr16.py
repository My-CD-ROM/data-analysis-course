import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, spearmanr

variant_number = 1
np.random.seed(variant_number)

city = "Київ"
monthly_temp = [-4, -3, 2, 9, 15, 19, 21, 20, 14, 8, 2, -2]
months = ["Січ", "Лют", "Бер", "Кві", "Тра", "Чер",
          "Лип", "Сер", "Вер", "Жов", "Лис", "Гру"]

rows = []
for month, temp in zip(months, monthly_temp):
    heating_days = np.clip(18 - temp + np.random.normal(0, 1.5), 0, 30)
    heating_days = round(heating_days)
    cost = 0.15 * heating_days + np.random.normal(0, 1.0)
    cost = round(max(cost, 0), 1)
    rows.append({
        "місто": city, "місяць": month, "температура": temp,
        "опалювальні_дні": heating_days, "витрати_на_опалення": cost,
    })

climate = pd.DataFrame(rows)
print("--- Вхідний датасет (climate) ---")
print(climate)

fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(climate["температура"], climate["витрати_на_опалення"], color='crimson', edgecolors='black', s=70)
ax.set_xlabel("Середньомісячна температура, °C", fontsize=11)
ax.set_ylabel("Витрати на опалення, тис. грн", fontsize=11)
ax.set_title("Залежність витрат на опалення від температури (м. Київ)", fontsize=12, fontweight='bold')
ax.grid(True, linestyle='--', alpha=0.6)

for i, row in climate.iterrows():
    ax.annotate(row["місяць"], (row["температура"], row["витрати_на_опалення"]),
                textcoords="offset points", xytext=(5, 5), ha='left', fontsize=8)

plt.tight_layout()
plt.show()

p_res = pearsonr(climate["температура"], climate["витрати_на_опалення"])
s_res = spearmanr(climate["температура"], climate["витрати_на_опалення"])

ci_p = p_res.confidence_interval(confidence_level=0.95)

print("\n=== ЗАВДАННЯ 2: Коефіцієнти кореляції ===")
print(f"Пірсон (r):   {p_res.statistic:.4f}, p-value = {p_res.pvalue:.4e}")
print(f"95% ДІ Пірсона: ({ci_p.low:.4f}, {ci_p.high:.4f})")
print(f"Спірмен (rho): {s_res.statistic:.4f}, p-value = {s_res.pvalue:.4e}")

df_three = climate[["температура", "опалювальні_дні", "витрати_на_опалення"]]

corr_pearson = df_three.corr(method="pearson")
corr_spearman = df_three.corr(method="spearman")

print("\n=== ЗАВДАННЯ 3: Кореляційна матриця (Пірсон) ===")
print(corr_pearson.round(4))

print("\n=== ЗАВДАННЯ 3: Кореляційна матриця (Спірмен) ===")
print(corr_spearman.round(4))

climate_outlier = climate.copy()
outlier_idx = 0
climate_outlier.loc[outlier_idx, "витрати_на_опалення"] *= 5

p_res_out = pearsonr(climate_outlier["температура"], climate_outlier["витрати_на_опалення"])
s_res_out = spearmanr(climate_outlier["температура"], climate_outlier["витрати_на_опалення"])

print("\n=== ЗАВДАННЯ 5: Кореляція з аномальним рядком (викидом) ===")
print(f"Нові витрати за Січень: {climate_outlier.loc[outlier_idx, 'витрати_на_опалення']} тис. грн")
print(f"Пірсон (r) з викидом:   {p_res_out.statistic:.4f}, p-value = {p_res_out.pvalue:.4e}")
print(f"Спірмен (rho) з викидом: {s_res_out.statistic:.4f}, p-value = {s_res_out.pvalue:.4e}")