import numpy as np
from scipy import stats

student_name = "Маневський Андрій"
group_name = "ІТ-32"
variant_number = 1
city = "Київ"
region = "Центр"
norma = 74.0

morning_temps = np.array([84, 82, 78, 70, 65, 63, 61, 63, 68, 75, 81, 85])

print("Завдання 1. Одновибірковий t-критерій проти норми")
t_stat_z1, p_val_z1 = stats.ttest_1samp(morning_temps, popmean=norma)
print(f"t-статистика: {t_stat_z1:.4f}")
print(f"p-value: {p_val_z1:.4f}")

print("\nЗавдання 2. Ручна перевірка t-статистики")
x_bar = morning_temps.mean()
s = morning_temps.std(ddof=1)
n = len(morning_temps)
t_manual = (x_bar - norma) / (s / np.sqrt(n))
print(f"Вибіркове середнє (x_bar): {x_bar:.4f}")
print(f"Вибіркове ст. відхилення (s): {s:.4f}")
print(f"Ручна t-статистика: {t_manual:.4f}")
print(f"Збіг з ttest_1samp: {np.isclose(t_stat_z1, t_manual)}")

lviv_temps = np.array([85, 83, 80, 73, 68, 65, 63, 65, 70, 77, 82, 86])

print("\nЗавдання 3. Незалежний двовибірковий критерій (Київ vs Львів)")
lev_stat_z3, lev_p_z3 = stats.levene(morning_temps, lviv_temps)
print(f"Критерій Лівена: stat = {lev_stat_z3:.4f}, p-value = {lev_p_z3:.4f}")

equal_var_z3 = lev_p_z3 >= 0.05
t_stat_z3, p_val_z3 = stats.ttest_ind(morning_temps, lviv_temps, equal_var=equal_var_z3)
print(f"Обрано equal_var = {equal_var_z3}")
print(f"ttest_ind: t = {t_stat_z3:.4f}, p-value = {p_val_z3:.4f}")

sumy_temps = np.array([85, 82, 77, 70, 64, 62, 60, 62, 68, 75, 81, 86])

print("\nЗавдання 4. Порівняння з іншим містом (Київ vs Суми)")
lev_stat_z4, lev_p_z4 = stats.levene(morning_temps, sumy_temps)
print(f"Критерій Лівена: stat = {lev_stat_z4:.4f}, p-value = {lev_p_z4:.4f}")

equal_var_z4 = lev_p_z4 >= 0.05
t_stat_z4, p_val_z4 = stats.ttest_ind(morning_temps, sumy_temps, equal_var=equal_var_z4)
print(f"Обрано equal_var = {equal_var_z4}")
print(f"ttest_ind: t = {t_stat_z4:.4f}, p-value = {p_val_z4:.4f}")

amplitude = np.array([3, 3, 4, 5, 6, 7, 7, 7, 6, 5, 4, 3])
evening_temps = morning_temps - amplitude

print("\nЗавдання 5. Парний t-критерій: ранок проти вечора")
t_stat_z5, p_val_z5 = stats.ttest_rel(morning_temps, evening_temps)
print("Вечірні значення:", evening_temps)
print(f"ttest_rel: t = {t_stat_z5:.4f}, p-value = {p_val_z5:.4f}")