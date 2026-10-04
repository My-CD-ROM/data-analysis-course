import numpy as np
from scipy import stats

# Дані варіанта 9 — Суми
sumy = np.array([85, 82, 77, 70, 64, 62, 60, 62, 68, 75, 81, 86])
norm = 73

# Завдання 1. Одновибірковий t-критерій
# H0: середня вологість Сум дорівнює нормі 73%.
# H1: середня вологість Сум відрізняється від норми 73%.

t_stat, p_value = stats.ttest_1samp(sumy, popmean=norm)

print("Завдання 1")
print("Середнє:", sumy.mean())
print("t =", t_stat)
print("p =", p_value)

# Завдання 2. Ручна перевірка t-статистики
mean = sumy.mean()
s = sumy.std(ddof=1)
n = len(sumy)

t_manual = (mean - norm) / (s / np.sqrt(n))

print("\nЗавдання 2")
print("s =", s)
print("t вручну =", t_manual)
print("t з ttest_1samp =", t_stat)

# Завдання 3. Суми проти Одеси
# Одеса — Південь, тобто інший регіон.
odesa = np.array([82, 80, 78, 74, 71, 69, 67, 68, 72, 76, 80, 83])

lev3_stat, lev3_p = stats.levene(sumy, odesa)

# p < 0.05 -> дисперсії різні -> Welch
t3, p3 = stats.ttest_ind(sumy, odesa, equal_var=False)

print("\nЗавдання 3")
print("Levene: statistic =", lev3_stat, "p =", lev3_p)
print("t =", t3, "p =", p3)

# Завдання 4. Суми проти Києва
# Київ — Центр, тобто інший регіон, ніж Одеса.
kyiv = np.array([84, 82, 78, 70, 65, 63, 61, 63, 68, 75, 81, 85])

lev4_stat, lev4_p = stats.levene(sumy, kyiv)

# p >= 0.05 -> немає підстав вважати дисперсії різними
# -> стандартний t-критерій
t4, p4 = stats.ttest_ind(sumy, kyiv, equal_var=True)

print("\nЗавдання 4")
print("Levene: statistic =", lev4_stat, "p =", lev4_p)
print("t =", t4, "p =", p4)

# Завдання 5. Парний t-критерій
amplitude = np.array([3, 3, 4, 5, 6, 7, 7, 7, 6, 5, 4, 3])
evening = sumy - amplitude

t5, p5 = stats.ttest_rel(sumy, evening)

print("\nЗавдання 5")
print("Вечірні значення:", evening)
print("t =", t5)
print("p =", p5)

