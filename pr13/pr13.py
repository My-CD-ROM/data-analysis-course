import numpy as np
from scipy import stats

student_name = "Маневський Андрій"
group_name = "ІТ-32"
variant_number = 1
city = "Київ"
july_gen_temp = 21.0
mu0 = 20.0

np.random.seed(variant_number)
daily_temps = np.random.normal(loc=july_gen_temp, scale=2.5, size=30)

print("Завдання 1. Вибірка і точкові оцінки")
print("Масив daily_temps:", daily_temps)
x_bar = daily_temps.mean()
s = daily_temps.std(ddof=1)
n = len(daily_temps)
print(f"Вибіркове середнє (x_bar): {x_bar:.4f} °C")
print(f"Вибіркове стандартне відхилення (s): {s:.4f} °C")

se = s / np.sqrt(n)
z_stat = (x_bar - mu0) / se
p_value = 1 - stats.norm.cdf(z_stat)

print("\nЗавдання 3. z-статистика і p-value")
print(f"Стандартна похибка (se): {se:.4f}")
print(f"z-статистика: {z_stat:.4f}")
print(f"p-value (однобічний тест): {p_value:.4f}")

alpha = 0.05
print("\nЗавдання 4. Рішення при alpha = 0.05")
if p_value < alpha:
    print(f"Рішення: p-value ({p_value:.4f}) < alpha (0.05) -> Відхиляємо H0.")
else:
    print(f"Рішення: p-value ({p_value:.4f}) >= alpha (0.05) -> Не відхиляємо H0.")

ci_lower = x_bar - 1.96 * se
ci_upper = x_bar + 1.96 * se

print("\nЗавдання 5. Перевірка через довірчий інтервал")
print(f"95% довірчий інтервал для середньої температури: ({ci_lower:.4f}, {ci_upper:.4f})")
print(f"Чи потрапляє mu0 = {mu0} в інтервал: {ci_lower <= mu0 <= ci_upper}")