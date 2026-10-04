import numpy as np
import matplotlib.pyplot as plt

# Варіант 9 — Суми

lam = 0.24
true_mean = 1 / lam

# Один генератор для всіх завдань
rng = np.random.default_rng(9)

print("Варіант 9 — Суми")
print("λ =", lam)
print("Теоретичне E[X] =", true_mean)


# 1  Закон великих чисел

print("\nЗАВДАННЯ 1")

for n in [5, 50, 500, 20_000]:

    sample = rng.exponential(
        scale=1 / lam,
        size=n
    )

    sample_mean = sample.mean()
    difference = abs(sample_mean - true_mean)

    print(
        f"n = {n:5d} | "
        f"x̄ = {sample_mean:.4f} | "
        f"|x̄ - E[X]| = {difference:.4f}"
    )


# 2 Вибірковий розподіл середнього

print("\nЗАВДАННЯ 2")

n_repeats = 10_000

means_n10 = rng.exponential(
    scale=1 / lam,
    size=(n_repeats, 10)
).mean(axis=1)

means_n300 = rng.exponential(
    scale=1 / lam,
    size=(n_repeats, 300)
).mean(axis=1)

print("n = 10:")
print("Середнє =", means_n10.mean())
print("Std =", means_n10.std())

print("\nn = 300:")
print("Середнє =", means_n300.mean())
print("Std =", means_n300.std())


fig, axes = plt.subplots(1, 2, figsize=(12, 4))

axes[0].hist(
    means_n10,
    bins=40,
    density=True,
    edgecolor="white"
)
axes[0].set_title("Вибірковий розподіл x̄, n = 10")
axes[0].set_xlabel("x̄")
axes[0].set_ylabel("Густина")

axes[1].hist(
    means_n300,
    bins=40,
    density=True,
    edgecolor="white"
)
axes[1].set_title("Вибірковий розподіл x̄, n = 300")
axes[1].set_xlabel("x̄")
axes[1].set_ylabel("Густина")

plt.tight_layout()
plt.show()


# 3 Стандартна похибка

print("\nЗАВДАННЯ 3")
print("n     Теоретична SE     Виміряна std")

for n in [10, 30, 100, 300]:

    se_theoretical = (1 / lam) / np.sqrt(n)

    sample_means = rng.exponential(
        scale=1 / lam,
        size=(10_000, n)
    ).mean(axis=1)

    se_simulated = sample_means.std()

    print(
        f"{n:<5d} "
        f"{se_theoretical:<18.4f} "
        f"{se_simulated:.4f}"
    )


# 4 Закон убуваючої віддачі
print("\nЗАВДАННЯ 4")

se_25 = (1 / lam) / np.sqrt(25)
se_100 = (1 / lam) / np.sqrt(100)

print("SE для n = 25:", se_25)
print("SE для n = 100:", se_100)
print("Відношення:", se_25 / se_100)


#5 n_repeats = 50

print("\nЗАВДАННЯ 5")

means_50 = rng.exponential(
    scale=1 / lam,
    size=(50, 10)
).mean(axis=1)

plt.figure(figsize=(8, 4))

plt.hist(
    means_50,
    bins=15,
    density=True,
    edgecolor="white"
)

plt.xlabel("x̄")
plt.ylabel("Густина")
plt.title("Вибірковий розподіл: n = 10, n_repeats = 50")

plt.show()
