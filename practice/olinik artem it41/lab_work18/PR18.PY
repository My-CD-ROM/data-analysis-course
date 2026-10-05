import random
import math

# ============================================================
# PRACTICAL WORK 18
# Multiple Linear Regression
# Student: Artem Oliinyk
# Group: IT-41
# Variant: 1
# City: Kyiv
# ============================================================

random.seed(42)

city = "Kyiv"
mean_temp = 9.5
amplitude = 14
hum_base = 74

months = list(range(1, 13))

temperature = []
humidity = []
heating_days = []
heating_cost = []

# ============================================================
# DATA GENERATION
# ============================================================

for month in months:

    temp = (
        mean_temp
        + amplitude * math.cos((month - 7) / 12 * 2 * math.pi)
        + random.gauss(0, 1.0)
    )

    hum = hum_base + random.gauss(0, 5.0)

    if temp < 8:
        days = 30
    elif temp < 12:
        days = 15
    else:
        days = 0

    cost = (
        200
        - 9.0 * temp
        + 0.6 * hum
        + 2.5 * days
        + random.gauss(0, 15)
    )

    temperature.append(round(temp, 1))
    humidity.append(round(hum, 1))
    heating_days.append(days)
    heating_cost.append(round(cost, 1))


print("=" * 75)
print("PRACTICAL WORK 18")
print("Student: Artem Oliinyk")
print("Group: IT-41")
print("Variant: 1")
print("City: Kyiv")
print("=" * 75)

print("\nDATASET:")

print(
    f"{'Month':<8}"
    f"{'Temp':>10}"
    f"{'Humidity':>12}"
    f"{'Heat days':>12}"
    f"{'Cost':>12}"
)

for m, t, h, d, c in zip(
    months,
    temperature,
    humidity,
    heating_days,
    heating_cost
):
    print(
        f"{m:<8}"
        f"{t:>10.1f}"
        f"{h:>12.1f}"
        f"{d:>12}"
        f"{c:>12.1f}"
    )


# ============================================================
# MATRIX FUNCTIONS
# ============================================================

def transpose(matrix):
    return [list(row) for row in zip(*matrix)]


def matrix_multiply(A, B):
    result = []

    for i in range(len(A)):
        row = []

        for j in range(len(B[0])):
            value = sum(
                A[i][k] * B[k][j]
                for k in range(len(B))
            )
            row.append(value)

        result.append(row)

    return result


def inverse_matrix(matrix):

    n = len(matrix)

    augmented = []

    for i in range(n):
        row = matrix[i][:]
        identity = [0.0] * n
        identity[i] = 1.0
        augmented.append(row + identity)

    for i in range(n):

        pivot = augmented[i][i]

        if abs(pivot) < 1e-12:

            for j in range(i + 1, n):
                if abs(augmented[j][i]) > 1e-12:
                    augmented[i], augmented[j] = (
                        augmented[j],
                        augmented[i]
                    )
                    pivot = augmented[i][i]
                    break

        for j in range(2 * n):
            augmented[i][j] /= pivot

        for k in range(n):

            if k == i:
                continue

            factor = augmented[k][i]

            for j in range(2 * n):
                augmented[k][j] -= (
                    factor * augmented[i][j]
                )

    return [
        row[n:]
        for row in augmented
    ]


# ============================================================
# OLS FUNCTION
# ============================================================

def ols(X, y):

    XT = transpose(X)

    XTX = matrix_multiply(XT, X)

    XTX_inv = inverse_matrix(XTX)

    y_matrix = [[value] for value in y]

    XTy = matrix_multiply(XT, y_matrix)

    beta_matrix = matrix_multiply(
        XTX_inv,
        XTy
    )

    beta = [
        row[0]
        for row in beta_matrix
    ]

    predicted = []

    for row in X:
        value = sum(
            b * x
            for b, x in zip(beta, row)
        )
        predicted.append(value)

    residuals = [
        actual - pred
        for actual, pred in zip(y, predicted)
    ]

    mean_y = sum(y) / len(y)

    ss_res = sum(
        r ** 2
        for r in residuals
    )

    ss_total = sum(
        (value - mean_y) ** 2
        for value in y
    )

    r_squared = 1 - ss_res / ss_total

    n = len(y)
    k = len(beta) - 1

    adjusted_r_squared = (
        1
        - (1 - r_squared)
        * (n - 1)
        / (n - k - 1)
    )

    return (
        beta,
        predicted,
        residuals,
        r_squared,
        adjusted_r_squared
    )


# ============================================================
# TASK 1
# MODEL WITH TWO PREDICTORS
# ============================================================

print("\n" + "=" * 75)
print("TASK 1. MODEL WITH TWO PREDICTORS")
print("=" * 75)

X2 = []

for temp, hum in zip(
    temperature,
    humidity
):
    X2.append([
        1.0,
        temp,
        hum
    ])

(
    beta2,
    predicted2,
    residuals2,
    r2_2,
    adj_r2_2
) = ols(
    X2,
    heating_cost
)

b0 = beta2[0]
b_temp = beta2[1]
b_hum = beta2[2]

print("\nRegression equation:")

print(
    f"Cost = {b0:.3f} "
    f"+ ({b_temp:.3f}) * Temperature "
    f"+ ({b_hum:.3f}) * Humidity"
)

print(f"\nIntercept = {b0:.3f}")
print(f"Temperature coefficient = {b_temp:.3f}")
print(f"Humidity coefficient = {b_hum:.3f}")

print(f"\nR^2 = {r2_2:.4f}")
print(f"Adjusted R^2 = {adj_r2_2:.4f}")


# ============================================================
# TASK 2
# COEFFICIENT INTERPRETATION
# ============================================================

print("\n" + "=" * 75)
print("TASK 2. COEFFICIENT INTERPRETATION")
print("=" * 75)

print(
    f"\nHolding humidity constant, "
    f"a 1 C increase in temperature changes "
    f"the predicted heating cost by "
    f"{b_temp:.3f} units."
)

print(
    f"\nHolding temperature constant, "
    f"a 1 percentage point increase in humidity "
    f"changes predicted heating cost by "
    f"{b_hum:.3f} units."
)

if b_temp < 0:
    print(
        "\nThe temperature coefficient is negative, "
        "which is logical: warmer weather reduces heating costs."
    )

if b_hum > 0:
    print(
        "The humidity coefficient is positive in this sample."
    )
else:
    print(
        "The humidity coefficient is negative in this sample."
    )


# ============================================================
# TASK 3
# VIF
# ============================================================

print("\n" + "=" * 75)
print("TASK 3. VIF")
print("=" * 75)


def simple_r_squared(x, y):

    mean_x = sum(x) / len(x)
    mean_y = sum(y) / len(y)

    numerator = sum(
        (a - mean_x) * (b - mean_y)
        for a, b in zip(x, y)
    )

    denominator = math.sqrt(
        sum((a - mean_x) ** 2 for a in x)
        *
        sum((b - mean_y) ** 2 for b in y)
    )

    r = numerator / denominator

    return r ** 2


r2_temp_hum = simple_r_squared(
    temperature,
    humidity
)

vif_temp = 1 / (1 - r2_temp_hum)
vif_hum = 1 / (1 - r2_temp_hum)

print(
    f"\nVIF Temperature = "
    f"{vif_temp:.3f}"
)

print(
    f"VIF Humidity = "
    f"{vif_hum:.3f}"
)

if vif_temp < 5:
    print(
        "\nVIF < 5. There is no serious "
        "multicollinearity problem."
    )

print(
    "This is expected because humidity is generated "
    "independently from temperature."
)


# ============================================================
# TASK 4
# MODEL WITH THREE PREDICTORS
# ============================================================

print("\n" + "=" * 75)
print("TASK 4. MODEL WITH THREE PREDICTORS")
print("=" * 75)

X3 = []

for temp, hum, days in zip(
    temperature,
    humidity,
    heating_days
):
    X3.append([
        1.0,
        temp,
        hum,
        days
    ])

(
    beta3,
    predicted3,
    residuals3,
    r2_3,
    adj_r2_3
) = ols(
    X3,
    heating_cost
)

print("\nRegression equation:")

print(
    f"Cost = {beta3[0]:.3f} "
    f"+ ({beta3[1]:.3f}) * Temperature "
    f"+ ({beta3[2]:.3f}) * Humidity "
    f"+ ({beta3[3]:.3f}) * HeatingDays"
)

print("\nMODEL COMPARISON:")

print(
    f"{'Model':<25}"
    f"{'R^2':>12}"
    f"{'Adjusted R^2':>18}"
)

print(
    f"{'2 predictors':<25}"
    f"{r2_2:>12.4f}"
    f"{adj_r2_2:>18.4f}"
)

print(
    f"{'3 predictors':<25}"
    f"{r2_3:>12.4f}"
    f"{adj_r2_3:>18.4f}"
)

print(
    "\nAdding HeatingDays cannot decrease ordinary R^2."
)

if adj_r2_3 > adj_r2_2:
    print(
        "Adjusted R^2 also increased, so the third "
        "predictor improves the model enough to justify "
        "the additional complexity."
    )
else:
    print(
        "Adjusted R^2 did not improve, so the third "
        "predictor does not justify the additional complexity."
    )

print(
    "Temperature and HeatingDays are strongly related "
    "because HeatingDays is determined from temperature."
)


# ============================================================
# TASK 5
# RESIDUAL DIAGNOSTICS
# ============================================================

print("\n" + "=" * 75)
print("TASK 5. RESIDUAL DIAGNOSTICS")
print("=" * 75)

print(
    f"\n{'Month':<8}"
    f"{'Predicted':>14}"
    f"{'Actual':>12}"
    f"{'Residual':>14}"
)

for month, pred, actual, residual in zip(
    months,
    predicted2,
    heating_cost,
    residuals2
):
    print(
        f"{month:<8}"
        f"{pred:>14.2f}"
        f"{actual:>12.2f}"
        f"{residual:>14.2f}"
    )


print("\nTEXT RESIDUAL PLOT:")
print("Negative <----------- 0 -----------> Positive\n")

max_abs = max(
    abs(r)
    for r in residuals2
)

for month, residual in zip(
    months,
    residuals2
):

    width = 41
    center = 20

    line = [" "] * width
    line[center] = "|"

    if max_abs > 0:
        offset = round(
            residual / max_abs * 18
        )
    else:
        offset = 0

    position = center + offset
    position = max(
        0,
        min(width - 1, position)
    )

    line[position] = "*"

    print(
        f"{month:>2} "
        + "".join(line)
        + f" {residual:>7.2f}"
    )


mean_residual = (
    sum(residuals2)
    / len(residuals2)
)

print(
    f"\nMean residual = "
    f"{mean_residual:.8f}"
)

print(
    "\nResiduals are distributed around zero."
)

print(
    "If the residual spread does not systematically "
    "increase or decrease with predicted values, there is "
    "no obvious funnel-shaped heteroscedasticity."
)

print(
    "\nNOTE:"
)

print(
    "The original assignment asks for QQ-plot and "
    "Shapiro-Wilk test using scipy."
)

print(
    "They are not executed in this version because Windows "
    "Application Control blocks scipy DLL files on this computer."
)


# ============================================================
# TASK 6
# SIMPLE VS MULTIPLE REGRESSION
# ============================================================

print("\n" + "=" * 75)
print("TASK 6. SIMPLE VS MULTIPLE REGRESSION")
print("=" * 75)

X1 = []

for temp in temperature:
    X1.append([
        1.0,
        temp
    ])

(
    beta1,
    predicted1,
    residuals1,
    r2_1,
    adj_r2_1
) = ols(
    X1,
    heating_cost
)

print(
    f"\nSimple regression "
    f"(Temperature only) R^2 = "
    f"{r2_1:.4f}"
)

print(
    f"Multiple regression "
    f"(Temperature + Humidity) R^2 = "
    f"{r2_2:.4f}"
)

print(
    f"Multiple regression Adjusted R^2 = "
    f"{adj_r2_2:.4f}"
)

difference = r2_2 - r2_1

print(
    f"\nR^2 improvement after adding humidity = "
    f"{difference:.4f}"
)

print(
    "\nOrdinary R^2 cannot decrease when another predictor "
    "is added because least squares can always assign that "
    "predictor a coefficient close to zero if it is not useful."
)

print(
    "Adjusted R^2 applies a penalty for additional predictors, "
    "so it is more appropriate for comparing models with "
    "different numbers of predictors."
)


# ============================================================
# CONTROL QUESTIONS
# ============================================================

print("\n" + "=" * 75)
print("CONTROL QUESTIONS")
print("=" * 75)

print("""
1. Why is a constant needed?

The constant represents the intercept of the regression model.
Without it, the regression equation is forced to pass through
zero, which can distort the estimated coefficients.


2. Multiple vs simple regression coefficient:

In simple regression, the coefficient describes the relationship
between one predictor and the dependent variable.

In multiple regression, each coefficient describes the effect
of its predictor while holding all other predictors constant.


3. Why cannot ordinary R^2 decrease?

When a new predictor is added, the model has more flexibility.
Least squares can always use the new predictor or effectively
ignore it. Therefore, the residual sum of squares cannot increase
and R^2 cannot decrease.

Adjusted R^2 includes a penalty for unnecessary predictors.


4. What does VIF mean?

VIF close to 1 indicates little or no multicollinearity.

VIF above 5 deserves attention.

VIF above 10 indicates serious multicollinearity and unstable
coefficient estimates. In practice, strongly redundant
predictors may need to be removed or reconsidered.
""")


# ============================================================
# FINAL RESULTS
# ============================================================

print("\n" + "=" * 75)
print("FINAL RESULTS")
print("=" * 75)

print("\nMODEL 1: Temperature + Humidity")

print(
    f"Cost = {beta2[0]:.3f} "
    f"+ ({beta2[1]:.3f}) * Temperature "
    f"+ ({beta2[2]:.3f}) * Humidity"
)

print(f"R^2 = {r2_2:.4f}")
print(f"Adjusted R^2 = {adj_r2_2:.4f}")

print("\nMODEL 2: Temperature + Humidity + HeatingDays")

print(
    f"Cost = {beta3[0]:.3f} "
    f"+ ({beta3[1]:.3f}) * Temperature "
    f"+ ({beta3[2]:.3f}) * Humidity "
    f"+ ({beta3[3]:.3f}) * HeatingDays"
)

print(f"R^2 = {r2_3:.4f}")
print(f"Adjusted R^2 = {adj_r2_3:.4f}")

print("\nPRACTICAL WORK 18 COMPLETED")
print("=" * 75)