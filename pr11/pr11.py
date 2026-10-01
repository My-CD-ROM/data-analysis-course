import numpy as np
import matplotlib.pyplot as plt

student_name = "Маневський Андрій"
group_name = "ІТ-32"
variant_number = 1
city = "Київ"
lam = 0.20
true_mean = 1 / lam

rng = np.random.default_rng(variant_number)

print("Завдання 1. Перевірка закону великих чисел")
n_values_z1 = [5, 50, 500, 20000]
for n in n_values_z1:
    sample = rng.exponential(scale=1 / lam, size=n)
    sample_mean = sample.mean()
    abs_diff = abs(sample_mean - true_mean)
    print(f"n = {n:5d} | Вибіркове середнє: {sample_mean:.4f} | Абсолютна різниця: {abs_diff:.4f}")

n_repeats = 10000
means_n10 = rng.exponential(scale=1 / lam, size=(n_repeats, 10)).mean(axis=1)
means_n300 = rng.exponential(scale=1 / lam, size=(n_repeats, 300)).mean(axis=1)

fig, axes = plt.subplots(1, 2, figsize=(12, 4))
axes[0].hist(means_n10, bins=50, density=True, color="skyblue", edgecolor="white")
axes[0].set_title(f"n = 10, std = {means_n10.std():.4f}")
axes[0].set_xlabel("Вибіркове середнє x̄")
axes[0].set_ylabel("Густина ймовірності")

axes[1].hist(means_n300, bins=50, density=True, color="coral", edgecolor="white")
axes[1].set_title(f"n = 300, std = {means_n300.std():.4f}")
axes[1].set_xlabel("Вибіркове середнє x̄")
axes[1].set_ylabel("Густина ймовірності")

plt.tight_layout()
plt.show()

print("\nЗавдання 3. Стандартна похибка: теорія проти симуляції")
n_values_z3 = [10, 30, 100, 300]
print(f"{'n':<6} | {'Теоретична SE':<15} | {'Виміряна std':<15}")
print("-" * 42)
for n in n_values_z3:
    se_theoretical = (1 / lam) / np.sqrt(n)
    sample_means = rng.exponential(scale=1 / lam, size=(n_repeats, n)).mean(axis=1)
    measured_std = sample_means.std()
    print(f"{n:<6} | {se_theoretical:<15.4f} | {measured_std:<15.4f}")

se_n25 = (1 / lam) / np.sqrt(25)
se_n100 = (1 / lam) / np.sqrt(100)
print("\nЗавдання 4. Закон убуваючої віддачі")
print(f"SE для n = 25:  {se_n25:.4f}")
print(f"SE для n = 100: {se_n100:.4f}")

means_n10_r50 = rng.exponential(scale=1 / lam, size=(50, 10)).mean(axis=1)
plt.figure(figsize=(6, 4))
plt.hist(means_n10_r50, bins=15, density=True, color="mediumpurple", edgecolor="white")
plt.title("n = 10, n_repeats = 50")
plt.xlabel("Вибіркове середнє x̄")
plt.ylabel("Густина ймовірності")
plt.tight_layout()
plt.show()