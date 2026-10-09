import numpy as np
from scipy.optimize import linprog

# ==========================================
# ВАРІАНТ 1 (Київ)
# ==========================================

# ------------------------------------------
# ЗАВДАННЯ 1 та 2: Розв'язання через linprog
# ------------------------------------------
# Цільова функція: Z = 60*x1 + 45*x2 -> max
# Оскільки linprog мінімізує, передаємо від'ємні коефіцієнти: [-60, -45]
c = [-60, -45]

# Матриця коефіцієнтів обмежень (A_ub @ x <= b_ub)
# 1. Сировина:     3*x1 + 5*x2 <= 300
# 2. Обладнання:   4*x1 + 2*x2 <= 220
# 3. Електроенергія: 1*x1 + 1*x2 <= 95
A_ub = [
    [3, 5],
    [4, 2],
    [1, 1]
]

b_ub = [300, 220, 95]

bounds = [(0, None), (0, None)]

res = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")

x1, x2 = res.x
max_profit = -res.fun

print("=== ЗАВДАННЯ 2: ОПТИМАЛЬНИЙ РОЗВ'ЯЗОК ===")
print(f"Статус оптимізації (res.status): {res.status}")
print(f"Повідомлення (res.message): {res.message}")
print(f"Кількість виробу А (x1): {x1:.4f} од.")
print(f"Кількість виробу Б (x2): {x2:.4f} од.")
print(f"Максимальний тижневий прибуток: {max_profit:.2f} грн")


# ------------------------------------------
# ЗАВДАННЯ 4: Аналіз активних обмежень (slack)
# ------------------------------------------
print("\n=== ЗАВДАННЯ 4: АНАЛІЗ РЕСУРСІВ (SLACK) ===")
resources = ["Сировина (кг)", "Час обладнання (год)", "Електроенергія (кВт·год)"]
for name, slack, limit in zip(resources, res.slack, b_ub):
    used = limit - slack
    status = "АКТИВНЕ (вузьке місце)" if np.isclose(slack, 0) else f"НЕАКТИВНЕ (запас {slack:.2f})"
    print(f"{name}: використано {used:.2f} з {limit} | Залишок (slack): {slack:.2f} -> {status}")


# ------------------------------------------
# ЗАВДАННЯ 5: What-if аналіз
# ------------------------------------------
print("\n=== ЗАВДАННЯ 5: WHAT-IF АНАЛІЗ ===")

# 1) Збільшення активного ресурсу на 15% (Час обладнання: 220 -> 253)
b_ub_active_increased = [300, 220 * 1.15, 95]
res_active_inc = linprog(c, A_ub=A_ub, b_ub=b_ub_active_increased, bounds=bounds, method="highs")

print("--- 1. Збільшення АКТИВНОГО ресурсу (Час обладнання +15%) ---")
print(f"Нові обсяги: x1 = {res_active_inc.x[0]:.4f}, x2 = {res_active_inc.x[1]:.4f}")
print(f"Новий прибуток: {-res_active_inc.fun:.2f} грн (зміна: {-res_active_inc.fun - max_profit:+.2f} грн)")

# 2) Збільшення неактивного ресурсу на 50% (Сировина: 300 -> 450)
b_ub_inactive_increased = [300 * 1.5, 220, 95]
res_inactive_inc = linprog(c, A_ub=A_ub, b_ub=b_ub_inactive_increased, bounds=bounds, method="highs")

print("\n--- 2. Збільшення НЕАКТИВНОГО ресурсу (Сировина +50%) ---")
print(f"Нові обсяги: x1 = {res_inactive_inc.x[0]:.4f}, x2 = {res_inactive_inc.x[1]:.4f}")
print(f"Новий прибуток: {-res_inactive_inc.fun:.2f} грн (зміна: {-res_inactive_inc.fun - max_profit:+.2f} грн)")