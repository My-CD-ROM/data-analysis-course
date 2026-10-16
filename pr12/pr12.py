import numpy as np
from scipy import stats

student_name = "Маневський Андрій"
group_name = "ІТ-32"
variant_number = 1
city = "Київ"
july_temp = 21.0

np.random.seed(variant_number)
daily_temps = np.random.normal(loc=july_temp, scale=2.5, size=30)

print("Завдання 1. Вибірка денних температур")
print("Масив daily_temps:", daily_temps)
print(f"Вибіркове середнє (mean): {daily_temps.mean():.4f}")
print(f"Вибіркове стандартне відхилення (s, ddof=1): {daily_temps.std(ddof=1):.4f}")

mean = daily_temps.mean()
s = daily_temps.std(ddof=1)
n = len(daily_temps)
se = s / np.sqrt(n)

ci_mean_95 = stats.t.interval(0.95, df=n - 1, loc=mean, scale=se)

print("\nЗавдання 2. Довірчий інтервал для середньої температури")
print(f"Стандартна похибка (se): {se:.4f}")
print(f"95% довірчий інтервал для середнього (t-розподіл): ({ci_mean_95[0]:.4f}, {ci_mean_95[1]:.4f})")

above_july = daily_temps > july_temp
p_hat = above_july.mean()
n_p = n * p_hat
n_1p = n * (1 - p_hat)

se_p = np.sqrt(p_hat * (1 - p_hat) / n)
ci_prop_95 = stats.norm.interval(0.95, loc=p_hat, scale=se_p)

print("\nЗавдання 3. Довірчий інтервал для частки")
print(f"Частка p_hat: {p_hat:.4f}")
print(f"Перевірка умов: n*p_hat = {n_p:.1f}, n*(1-p_hat) = {n_1p:.1f}")
print(f"95% довірчий інтервал для частки: ({ci_prop_95[0]:.4f}, {ci_prop_95[1]:.4f})")
print(f"Чи потрапляє 0.5 в інтервал: {ci_prop_95[0] <= 0.5 <= ci_prop_95[1]}")

ci_90 = stats.t.interval(0.90, df=n - 1, loc=mean, scale=se)
ci_95 = stats.t.interval(0.95, df=n - 1, loc=mean, scale=se)
ci_99 = stats.t.interval(0.99, df=n - 1, loc=mean, scale=se)

w_90 = ci_90[1] - ci_90[0]
w_95 = ci_95[1] - ci_95[0]
w_99 = ci_99[1] - ci_99[0]

print("\nЗавдання 4. Ширина інтервалу при різних рівнях довіри")
print(f"{'Рівень довіри':<15} | {'Нижня межа':<12} | {'Верхня межа':<12} | {'Ширина інтервалу':<15}")
print("-" * 62)
print(f"{'90%':<15} | {ci_90[0]:<12.4f} | {ci_90[1]:<12.4f} | {w_90:<15.4f}")
print(f"{'95%':<15} | {ci_95[0]:<12.4f} | {ci_95[1]:<12.4f} | {w_95:<15.4f}")
print(f"{'99%':<15} | {ci_99[0]:<12.4f} | {ci_99[1]:<12.4f} | {w_99:<15.4f}")