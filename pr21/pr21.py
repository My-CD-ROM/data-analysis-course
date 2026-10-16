import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Фіксація генератора випадкових чисел за номером варіанта (Варіант 1)
VARIANT = 1
EXACT_VALUE = np.pi / 4

# --- Завдання 1: Оцінка для N = 1000 ---
np.random.seed(VARIANT)
N_1000 = 1000
x_1000 = np.random.uniform(0, 1, size=N_1000)
y_1000 = np.random.uniform(0, 1, size=N_1000)

inside_1000 = (x_1000**2 + y_1000**2) <= 1.0
estimate_1000 = np.mean(inside_1000) * 1.0  # Площа квадрата S = 1

print(f"=== ЗАВДАННЯ 1 ===")
print(f"Оцінка методом Монте-Карло (N = 1000): {estimate_1000:.6f}")

# --- Завдання 2: Порівняння з точним значенням ---
abs_error_1000 = abs(estimate_1000 - EXACT_VALUE)
rel_error_1000 = (abs_error_1000 / EXACT_VALUE) * 100

print(f"\n=== ЗАВДАННЯ 2 ===")
print(f"Точне значення (pi / 4): {EXACT_VALUE:.6f}")
print(f"Абсолютна похибка (N = 1000): {abs_error_1000:.6f}")
print(f"Відносна похибка: {rel_error_1000:.2f}%")

# --- Завдання 3: Дослідження збіжності за N ---
N_values = [100, 1_000, 10_000, 100_000]
results = []

for N in N_values:
    np.random.seed(VARIANT)
    x = np.random.uniform(0, 1, size=N)
    y = np.random.uniform(0, 1, size=N)
    inside = (x**2 + y**2) <= 1.0
    estimate = np.mean(inside) * 1.0
    abs_err = abs(estimate - EXACT_VALUE)
    rel_err = (abs_err / EXACT_VALUE) * 100
    results.append({
        "N": N,
        "Оцінка": round(estimate, 6),
        "Абсолютна похибка": round(abs_err, 6),
        "Відносна похибка (%)": round(rel_err, 2)
    })

df_results = pd.DataFrame(results)

print(f"\n=== ЗАВДАННЯ 3: ТАБЛИЦЯ ЗБІЖНОСТІ ===")
print(df_results.to_string(index=False))

# --- Завдання 4: Побудова графіка похибки ---
fig, ax = plt.subplots(figsize=(8, 5))

ax.plot(df_results["N"], df_results["Абсолютна похибка"], 'ro-', label="Фактична похибка Монте-Карло")

# Теоретична крива 1/sqrt(N), масштабована для наочності порівняння
c_scale = df_results.loc[df_results["N"] == 100, "Абсолютна похибка"].values[0] * np.sqrt(100)
theoretical_curve = c_scale / np.sqrt(N_values)
ax.plot(N_values, theoretical_curve, 'k--', label=r"Теоретичний тренд $\propto 1/\sqrt{N}$")

ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlabel("Кількість випробувань (N)", fontsize=11)
ax.set_ylabel("Абсолютна похибка", fontsize=11)
ax.set_title("Залежність абсолютної похибки від кількості випробувань N (Варіант 1 — Київ)", fontsize=12)
ax.grid(True, which="both", linestyle=":", alpha=0.7)
ax.legend(fontsize=10)

plt.tight_layout()
plt.show()