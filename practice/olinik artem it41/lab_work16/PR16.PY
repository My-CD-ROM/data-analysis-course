import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, spearmanr

# ============================================================
# PRACTICAL WORK 16
# Correlation analysis
# Student: Artem Oliinyk
# Group: IT-41
# Variant: 1
# City: Kyiv
# ============================================================

np.random.seed(1)

city = "Kyiv"

months = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]

# Variant 1 - Kyiv
monthly_temp = [-4, -3, 2, 9, 15, 19, 21, 20, 14, 8, 2, -2]

# ============================================================
# DATA GENERATION
# ============================================================

rows = []

for month, temp in zip(months, monthly_temp):
    heating_days = np.clip(
        18 - temp + np.random.normal(0, 1.5),
        0,
        30
    )
    heating_days = round(heating_days)

    cost = 0.15 * heating_days + np.random.normal(0, 1.0)
    cost = round(max(cost, 0), 1)

    rows.append({
        "city": city,
        "month": month,
        "temperature": temp,
        "heating_days": heating_days,
        "heating_cost": cost
    })

climate = pd.DataFrame(rows)

print("=" * 70)
print("PRACTICAL WORK 16")
print("Student: Artem Oliinyk")
print("Group: IT-41")
print("Variant: 1")
print("City: Kyiv")
print("=" * 70)

print("\nDATASET:")
print(climate.to_string(index=False))


# ============================================================
# TASK 1
# SCATTER PLOT
# ============================================================

print("\n" + "=" * 70)
print("TASK 1. SCATTER PLOT")
print("=" * 70)

plt.figure(figsize=(9, 6))

plt.scatter(
    climate["temperature"],
    climate["heating_cost"],
    s=70
)

plt.xlabel("Temperature, C")
plt.ylabel("Heating cost, thousand UAH")
plt.title("Heating cost vs temperature - Kyiv")
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print(
    "\nConclusion:"
    "\nThe scatter plot shows a negative relationship."
    "\nWhen temperature increases, heating costs generally decrease."
    "\nThe relationship is approximately linear, although random noise is present."
    "\nThis agrees with the data generation formula."
)


# ============================================================
# TASK 2
# PEARSON AND SPEARMAN CORRELATION
# ============================================================

print("\n" + "=" * 70)
print("TASK 2. PEARSON AND SPEARMAN CORRELATION")
print("=" * 70)

x = climate["temperature"]
y = climate["heating_cost"]

pearson_result = pearsonr(x, y)
spearman_result = spearmanr(x, y)

print(f"\nPearson r = {pearson_result.statistic:.4f}")
print(f"Pearson p-value = {pearson_result.pvalue:.6f}")

print(f"\nSpearman rho = {spearman_result.statistic:.4f}")
print(f"Spearman p-value = {spearman_result.pvalue:.6f}")

alpha = 0.05

print("\nHypothesis testing:")

if pearson_result.pvalue < alpha:
    print("Pearson: p < 0.05 -> reject H0.")
    print("There is a statistically significant correlation.")
else:
    print("Pearson: p >= 0.05 -> do not reject H0.")

if spearman_result.pvalue < alpha:
    print("Spearman: p < 0.05 -> reject H0.")
    print("There is a statistically significant monotonic correlation.")
else:
    print("Spearman: p >= 0.05 -> do not reject H0.")


# 95% confidence interval for Pearson correlation

try:
    ci = pearson_result.confidence_interval(confidence_level=0.95)

    print("\n95% confidence interval for Pearson r:")
    print(f"[{ci.low:.4f}; {ci.high:.4f}]")

except AttributeError:
    print("\nConfidence interval is unavailable in this SciPy version.")


print(
    "\nInterpretation:"
    "\nPearson and Spearman coefficients are both expected to be negative."
    "\nTheir similar values indicate that the relationship is approximately"
    "\nlinear and monotonic. As temperature increases, heating costs decrease."
)


# ============================================================
# TASK 3
# CORRELATION MATRIX
# ============================================================

print("\n" + "=" * 70)
print("TASK 3. CORRELATION MATRIX")
print("=" * 70)

numeric_data = climate[
    ["temperature", "heating_days", "heating_cost"]
]

pearson_matrix = numeric_data.corr()

print("\nPearson correlation matrix:")
print(pearson_matrix.round(4))

spearman_matrix = numeric_data.corr(method="spearman")

print("\nSpearman correlation matrix:")
print(spearman_matrix.round(4))


# Find strongest and weakest correlations

pairs = {
    "temperature - heating_days":
        abs(pearson_matrix.loc["temperature", "heating_days"]),

    "temperature - heating_cost":
        abs(pearson_matrix.loc["temperature", "heating_cost"]),

    "heating_days - heating_cost":
        abs(pearson_matrix.loc["heating_days", "heating_cost"])
}

strongest = max(pairs, key=pairs.get)
weakest = min(pairs, key=pairs.get)

print("\nStrongest correlation:")
print(strongest, "=", round(pairs[strongest], 4))

print("\nWeakest correlation:")
print(weakest, "=", round(pairs[weakest], 4))

print(
    "\nConclusion:"
    "\nThe strong correlations are expected because heating_days"
    "\nis calculated using temperature, while heating_cost is calculated"
    "\nusing heating_days. The Spearman matrix leads to similar conclusions."
)


# ============================================================
# TASK 4
# CORRELATION AND CAUSALITY
# ============================================================

print("\n" + "=" * 70)
print("TASK 4. CORRELATION AND CAUSALITY")
print("=" * 70)

print(
    "\nIn this dataset the relationship is not only an accidental correlation."
    "\nHeating days are directly calculated from temperature in the generation"
    "\nformula, and heating costs are then calculated from heating days."
    "\nTherefore temperature directly influences the generated values."
    "\nUnlike the classic ice cream and drowning example, there is no hidden"
    "\nconfounder responsible for the main relationship in this synthetic dataset."
)


# ============================================================
# TASK 5
# OUTLIER TEST
# ============================================================

print("\n" + "=" * 70)
print("TASK 5. OUTLIER TEST")
print("=" * 70)

# Copy original dataset
climate_outlier = climate.copy()

# Add anomalous observation
# Boiler accident caused heating costs to increase 5 times.

anomaly = pd.DataFrame([{
    "city": city,
    "month": "Emergency",
    "temperature": 5,
    "heating_days": 15,
    "heating_cost": climate["heating_cost"].max() * 5
}])

climate_outlier = pd.concat(
    [climate_outlier, anomaly],
    ignore_index=True
)

print("\nDataset with outlier:")
print(climate_outlier.to_string(index=False))


# New correlations

pearson_outlier = pearsonr(
    climate_outlier["temperature"],
    climate_outlier["heating_cost"]
)

spearman_outlier = spearmanr(
    climate_outlier["temperature"],
    climate_outlier["heating_cost"]
)

print("\nWITHOUT OUTLIER:")
print(f"Pearson r = {pearson_result.statistic:.4f}")
print(f"Spearman rho = {spearman_result.statistic:.4f}")

print("\nWITH OUTLIER:")
print(f"Pearson r = {pearson_outlier.statistic:.4f}")
print(f"Spearman rho = {spearman_outlier.statistic:.4f}")


pearson_change = abs(
    pearson_outlier.statistic - pearson_result.statistic
)

spearman_change = abs(
    spearman_outlier.statistic - spearman_result.statistic
)

print("\nChange in coefficients:")
print(f"Pearson change = {pearson_change:.4f}")
print(f"Spearman change = {spearman_change:.4f}")


if pearson_change > spearman_change:
    print(
        "\nPearson changed more strongly."
        "\nThis is expected because Pearson correlation uses the actual"
        "\nnumerical values and is more sensitive to extreme observations."
        "\nSpearman uses ranks, so one extreme value usually has less influence."
    )
else:
    print(
        "\nSpearman changed more strongly in this generated sample."
        "\nHowever, in general Pearson is more sensitive to extreme values,"
        "\nwhile Spearman is based on ranks and is usually more robust."
    )


# Plot with outlier

plt.figure(figsize=(9, 6))

plt.scatter(
    climate_outlier["temperature"],
    climate_outlier["heating_cost"],
    s=70
)

plt.xlabel("Temperature, C")
plt.ylabel("Heating cost, thousand UAH")
plt.title("Heating cost vs temperature with outlier - Kyiv")
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()


# ============================================================
# CONTROL QUESTIONS
# ============================================================

print("\n" + "=" * 70)
print("CONTROL QUESTIONS")
print("=" * 70)

print("""
1. Why does Pearson correlation use standard deviations?

Pearson correlation divides covariance by the product of the standard
deviations of both variables. This normalizes the covariance and makes
the coefficient independent of measurement units. The result is always
between -1 and 1.

2. Why does Spearman use ranks?

Spearman correlation replaces actual values with their ranks.
Therefore, extremely large or small numerical values have less influence
on the result. It measures the strength of a monotonic relationship.

3. Example where r is close to zero but a strong relationship exists:

For example, y = x^2 for values of x distributed symmetrically around zero.
There is a strong nonlinear relationship between x and y, but Pearson
correlation can be close to zero because it measures linear association.

4. Why does correlation not prove causation?

Two variables can be strongly correlated because of a third variable,
reverse causality, coincidence, or another hidden factor. Therefore,
correlation alone does not prove that changing one variable causes
changes in the other.
""")

print("=" * 70)
print("PRACTICAL WORK 16 COMPLETED")
print("=" * 70)