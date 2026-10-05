from scipy.optimize import linprog

# ============================================================
# PRACTICAL WORK 20
# Linear Programming
# Student: Artem Oliinyk
# Group: IT-41
# Variant: 1
# City: Kyiv
# ============================================================

# Variables:
# x1 - number of product A units per week
# x2 - number of product B units per week
#
# Maximize:
# 60*x1 + 45*x2
#
# Constraints:
# 3*x1 + 5*x2 <= 300   raw material
# 4*x1 + 2*x2 <= 220   machine time
# 1*x1 + 1*x2 <= 95    electricity
# x1 >= 0, x2 >= 0


# ------------------------------------------------------------
# TASK 2. Solve the original problem
# ------------------------------------------------------------

# linprog minimizes, so profit coefficients are negative
c = [-60, -45]

A_ub = [
    [3, 5],   # raw material
    [4, 2],   # machine time
    [1, 1]    # electricity
]

b_ub = [
    300,  # kg
    220,  # hours
    95    # kWh
]

bounds = [
    (0, None),
    (0, None)
]

res = linprog(
    c,
    A_ub=A_ub,
    b_ub=b_ub,
    bounds=bounds,
    method="highs"
)

print("=" * 65)
print("PRACTICAL WORK 20")
print("Student: Artem Oliinyk")
print("Group: IT-41")
print("Variant: 1")
print("City: Kyiv")
print("=" * 65)

print("\nTASK 2. ORIGINAL PROBLEM")
print("-" * 65)

print("res.x =", res.x)
print("res.fun =", res.fun)
print("res.status =", res.status)
print("res.message =", res.message)

if res.status == 0:
    print("\nOptimization completed successfully.")
else:
    print("\nOptimization failed.")

x1 = res.x[0]
x2 = res.x[1]
profit = -res.fun

print("\nTASK 3. INTERPRETATION")
print("-" * 65)

print(f"Product A: {x1:.4f} units/week")
print(f"Product B: {x2:.4f} units/week")
print(f"Maximum profit: {profit:.2f} UAH/week")

print(
    "\nThe linear programming model allows fractional values. "
    "In real production, products may need integer quantities. "
    "Simple rounding does not always guarantee the best integer solution."
)


# ------------------------------------------------------------
# TASK 4. Active constraints
# ------------------------------------------------------------

print("\nTASK 4. CONSTRAINTS")
print("-" * 65)

resource_names = [
    "Raw material",
    "Machine time",
    "Electricity"
]

units = [
    "kg",
    "hours",
    "kWh"
]

usage = [
    3 * x1 + 5 * x2,
    4 * x1 + 2 * x2,
    x1 + x2
]

for i in range(3):
    print(f"\n{resource_names[i]}:")
    print(f"  Used:  {usage[i]:.4f} {units[i]}")
    print(f"  Limit: {b_ub[i]:.4f} {units[i]}")
    print(f"  Slack: {res.slack[i]:.4f} {units[i]}")

    if abs(res.slack[i]) < 1e-7:
        print("  Status: ACTIVE constraint")
    else:
        print("  Status: INACTIVE constraint")


# ------------------------------------------------------------
# TASK 5.1
# Increase active resource (raw material) by 15%
# ------------------------------------------------------------

print("\n" + "=" * 65)
print("TASK 5.1. RAW MATERIAL LIMIT +15%")
print("=" * 65)

new_raw_material = 300 * 1.15

b_active = [
    new_raw_material,
    220,
    95
]

res_active = linprog(
    c,
    A_ub=A_ub,
    b_ub=b_active,
    bounds=bounds,
    method="highs"
)

print(f"Old raw material limit: 300 kg")
print(f"New raw material limit: {new_raw_material:.2f} kg")

print("\nNew res.x =", res_active.x)
print("New res.fun =", res_active.fun)
print("New res.status =", res_active.status)
print("New res.message =", res_active.message)

new_profit_active = -res_active.fun

print(f"\nProduct A: {res_active.x[0]:.4f} units/week")
print(f"Product B: {res_active.x[1]:.4f} units/week")
print(f"New maximum profit: {new_profit_active:.2f} UAH/week")

print(
    f"Profit increase: "
    f"{new_profit_active - profit:.2f} UAH/week"
)

print("Slack:", res_active.slack)


# ------------------------------------------------------------
# TASK 5.2
# Increase inactive resource (electricity) by 50%
# ------------------------------------------------------------

print("\n" + "=" * 65)
print("TASK 5.2. ELECTRICITY LIMIT +50%")
print("=" * 65)

new_electricity = 95 * 1.50

b_inactive = [
    300,
    220,
    new_electricity
]

res_inactive = linprog(
    c,
    A_ub=A_ub,
    b_ub=b_inactive,
    bounds=bounds,
    method="highs"
)

print(f"Old electricity limit: 95 kWh")
print(f"New electricity limit: {new_electricity:.2f} kWh")

print("\nNew res.x =", res_inactive.x)
print("New res.fun =", res_inactive.fun)
print("New res.status =", res_inactive.status)
print("New res.message =", res_inactive.message)

new_profit_inactive = -res_inactive.fun

print(f"\nProduct A: {res_inactive.x[0]:.4f} units/week")
print(f"Product B: {res_inactive.x[1]:.4f} units/week")
print(f"New maximum profit: {new_profit_inactive:.2f} UAH/week")

print(
    f"Profit change: "
    f"{new_profit_inactive - profit:.2f} UAH/week"
)

print("Slack:", res_inactive.slack)


# ------------------------------------------------------------
# FINAL SUMMARY
# ------------------------------------------------------------

print("\n" + "=" * 65)
print("FINAL SUMMARY")
print("=" * 65)

print(f"""
Original solution:
Product A = {x1:.4f}
Product B = {x2:.4f}
Maximum profit = {profit:.2f} UAH/week

Active constraints:
- Raw material
- Machine time

Inactive constraint:
- Electricity

After increasing raw material by 15%:
Product A = {res_active.x[0]:.4f}
Product B = {res_active.x[1]:.4f}
Profit = {new_profit_active:.2f} UAH/week

After increasing electricity by 50%:
Product A = {res_inactive.x[0]:.4f}
Product B = {res_inactive.x[1]:.4f}
Profit = {new_profit_inactive:.2f} UAH/week
""")