import numpy as np
import matplotlib.pyplot as plt
import math

# ============================================================
# PRACTICAL WORK 21
# Monte Carlo Method
# Student: Artem Oliinyk
# Group: IT-41
# Variant: 1
# City: Kyiv
# ============================================================

VARIANT = 1
EXACT = math.pi / 4


def monte_carlo_area(n):
    # Seed must be fixed before every simulation
    np.random.seed(VARIANT)

    # Generate random points in [0, 1] x [0, 1]
    x = np.random.uniform(0, 1, n)
    y = np.random.uniform(0, 1, n)

    # Check which points are inside the quarter circle
    inside = (x**2 + y**2) <= 1

    # Area of the square is 1,
    # so area estimate = fraction of points inside
    estimate = np.mean(inside) * 1.0

    return estimate


print("=" * 65)
print("PRACTICAL WORK 21")
print("Student: Artem Oliinyk")
print("Group: IT-41")
print("Variant: 1")
print("City: Kyiv")
print("Task type: Area")
print("=" * 65)


# ============================================================
# TASK 1
# ============================================================

print("\nTASK 1. MONTE CARLO ESTIMATE")
print("-" * 65)

N = 1000
estimate = monte_carlo_area(N)

print(f"N = {N}")
print(f"Monte Carlo estimate = {estimate:.6f}")
print(f"Exact value pi/4 = {EXACT:.6f}")


# ============================================================
# TASK 2
# ============================================================

print("\nTASK 2. COMPARISON WITH EXACT VALUE")
print("-" * 65)

absolute_error = abs(estimate - EXACT)
relative_error = absolute_error / EXACT * 100

print(f"Estimate       = {estimate:.6f}")
print(f"Exact value    = {EXACT:.6f}")
print(f"Absolute error = {absolute_error:.6f}")
print(f"Relative error = {relative_error:.4f}%")

print(
    "\nFor N = 1000 the error is relatively small. "
    "However, Monte Carlo simulation is random, so the estimate "
    "does not exactly equal the analytical value."
)


# ============================================================
# TASK 3
# Convergence
# ============================================================

print("\nTASK 3. CONVERGENCE")
print("-" * 65)

N_values = [100, 1000, 10000, 100000]

estimates = []
errors = []

print(f"{'N':>10} {'Estimate':>15} {'Absolute error':>20}")
print("-" * 50)

for n in N_values:
    current_estimate = monte_carlo_area(n)
    current_error = abs(current_estimate - EXACT)

    estimates.append(current_estimate)
    errors.append(current_error)

    print(
        f"{n:>10} "
        f"{current_estimate:>15.6f} "
        f"{current_error:>20.6f}"
    )


print("\nConvergence analysis:")

if errors[2] != 0:
    error_reduction = errors[0] / errors[2]

    print(
        f"From N = 100 to N = 10000, "
        f"N increased 100 times."
    )

    print(
        f"The error changed approximately "
        f"{error_reduction:.2f} times."
    )

print(
    "According to Monte Carlo theory, the typical error "
    "decreases proportionally to 1/sqrt(N)."
)

print(
    "Therefore, increasing N by 100 times should reduce "
    "the typical error by about sqrt(100) = 10 times."
)

print(
    "A single random simulation does not have to show "
    "exactly a 10-fold reduction because random fluctuations remain."
)


# ============================================================
# TASK 4
# Error graph
# ============================================================

print("\nTASK 4. ERROR GRAPH")
print("-" * 65)

fig, ax = plt.subplots()

ax.plot(
    N_values,
    errors,
    marker="o",
    label="Absolute error"
)

ax.set_xscale("log")

ax.set_xlabel("Number of trials N")
ax.set_ylabel("Absolute error")
ax.set_title("Monte Carlo error depending on N")

ax.grid(True)
ax.legend()

plt.tight_layout()
plt.show()

print(
    "The graph shows the general tendency of the error "
    "to decrease as N increases."
)

print(
    "Because Monte Carlo simulation is random, the error "
    "does not have to decrease strictly at every step."
)


# ============================================================
# TASK 5
# Law of Large Numbers and Central Limit Theorem
# ============================================================

print("\nTASK 5. LLN AND CLT")
print("-" * 65)

print(
    """
The Monte Carlo estimate is a sample mean of independent
random indicator variables.

For every generated point:

1 - the point is inside the quarter circle;
0 - the point is outside the quarter circle.

The Law of Large Numbers guarantees that the sample mean
approaches the true probability as N increases.

Since the square has area 1, this probability is equal to
the area of the quarter circle.

The Central Limit Theorem explains the statistical behavior
of the sample mean and why its standard error is proportional
to 1/sqrt(N).

Therefore, if the number of trials increases 4 times,
the typical error decreases approximately 2 times.

If the number of trials increases 100 times,
the typical error decreases approximately 10 times,
not 100 times.
"""
)


# ============================================================
# FINAL SUMMARY
# ============================================================

print("=" * 65)
print("FINAL SUMMARY")
print("=" * 65)

print(f"Variant: {VARIANT}")
print("City: Kyiv")
print("Figure: Quarter circle")
print("Condition: x^2 + y^2 <= 1")
print(f"Exact area: pi/4 = {EXACT:.6f}")

print("\nMonte Carlo results:")

for n, est, err in zip(N_values, estimates, errors):
    print(
        f"N = {n:>6}: "
        f"estimate = {est:.6f}, "
        f"error = {err:.6f}"
    )

print(
    "\nConclusion: increasing the number of trials generally "
    "improves the Monte Carlo estimate. The typical error "
    "decreases proportionally to 1/sqrt(N)."
)