import math
import random

# ============================================================
# PRACTICAL WORK 17
# Simple Linear Regression
# Student: Artem Oliinyk
# Group: IT-41
# Variant: 1
# City: Kyiv
# ============================================================

random.seed(1)

city = "Kyiv"

months = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]

# Variant 1 - Kyiv
temperature = [-4, -3, 2, 9, 15, 19, 21, 20, 14, 8, 2, -2]

# ============================================================
# DATA GENERATION
# ============================================================

heating_days = []
heating_cost = []

for temp in temperature:

    days = 18 - temp + random.gauss(0, 1.5)
    days = max(0, min(30, days))
    days = round(days)

    cost = 0.15 * days + random.gauss(0, 1.0)
    cost = round(max(cost, 0), 1)

    heating_days.append(days)
    heating_cost.append(cost)


print("=" * 70)
print("PRACTICAL WORK 17")
print("Student: Artem Oliinyk")
print("Group: IT-41")
print("Variant: 1")
print("City: Kyiv")
print("=" * 70)

print("\nDATASET:")

print(
    f"{'Month':<10}"
    f"{'Temp':>10}"
    f"{'Heating days':>16}"
    f"{'Cost':>12}"
)

for month, temp, days, cost in zip(
    months,
    temperature,
    heating_days,
    heating_cost
):
    print(
        f"{month:<10}"
        f"{temp:>10.1f}"
        f"{days:>16}"
        f"{cost:>12.1f}"
    )


# ============================================================
# TASK 1
# LINEAR REGRESSION
# ============================================================

print("\n" + "=" * 70)
print("TASK 1. LINEAR REGRESSION")
print("=" * 70)

x = temperature
y = heating_cost

n = len(x)

mean_x = sum(x) / n
mean_y = sum(y) / n

ss_xx = sum((xi - mean_x) ** 2 for xi in x)

ss_xy = sum(
    (xi - mean_x) * (yi - mean_y)
    for xi, yi in zip(x, y)
)

slope = ss_xy / ss_xx

intercept = mean_y - slope * mean_x

print(f"\nSlope b1 = {slope:.3f}")
print(f"Intercept b0 = {intercept:.3f}")

print(
    f"\nRegression equation:\n"
    f"Heating cost = {intercept:.3f} "
    f"+ ({slope:.3f}) * temperature"
)

if slope < 0:
    print(
        f"\nWhen temperature increases by 1 C, "
        f"heating cost decreases on average by "
        f"{abs(slope):.3f} thousand UAH."
    )
else:
    print(
        f"\nWhen temperature increases by 1 C, "
        f"heating cost increases on average by "
        f"{slope:.3f} thousand UAH."
    )

print(
    "The negative slope is logical because higher "
    "temperatures require less heating."
)


# ============================================================
# PREDICTIONS
# ============================================================

predicted = [
    intercept + slope * xi
    for xi in x
]

print("\nPredicted values:")

for month, actual, pred in zip(months, y, predicted):
    print(
        f"{month:<5} "
        f"actual={actual:>5.2f} "
        f"predicted={pred:>6.2f}"
    )


# ============================================================
# TASK 2
# R-SQUARED
# ============================================================

print("\n" + "=" * 70)
print("TASK 2. R-SQUARED")
print("=" * 70)

ss_res = sum(
    (actual - pred) ** 2
    for actual, pred in zip(y, predicted)
)

ss_total = sum(
    (yi - mean_y) ** 2
    for yi in y
)

r_squared = 1 - ss_res / ss_total

print(f"\nSS residual = {ss_res:.6f}")
print(f"SS total = {ss_total:.6f}")

print(f"\nR^2 = {r_squared:.6f}")


# ============================================================
# PEARSON CORRELATION MANUALLY
# ============================================================

ss_yy = sum(
    (yi - mean_y) ** 2
    for yi in y
)

pearson_r = ss_xy / math.sqrt(ss_xx * ss_yy)

print(f"Pearson r = {pearson_r:.6f}")
print(f"Pearson r^2 = {pearson_r ** 2:.6f}")

print(
    "\nFor simple linear regression:"
    "\nR^2 = Pearson r^2"
)

explained = r_squared * 100
unexplained = (1 - r_squared) * 100

print(
    f"\nTemperature explains approximately "
    f"{explained:.2f}% of variation in heating costs."
)

print(
    f"The remaining {unexplained:.2f}% "
    f"is not explained by this linear model."
)


# ============================================================
# TASK 3
# RESIDUALS
# ============================================================

print("\n" + "=" * 70)
print("TASK 3. RESIDUALS")
print("=" * 70)

residuals = [
    actual - pred
    for actual, pred in zip(y, predicted)
]

print(
    f"\n{'Month':<8}"
    f"{'Temp':>8}"
    f"{'Actual':>10}"
    f"{'Predicted':>12}"
    f"{'Residual':>12}"
)

for month, temp, actual, pred, residual in zip(
    months,
    x,
    y,
    predicted,
    residuals
):
    print(
        f"{month:<8}"
        f"{temp:>8.1f}"
        f"{actual:>10.2f}"
        f"{pred:>12.2f}"
        f"{residual:>12.3f}"
    )


print("\nResidual analysis:")

print(
    "The residuals contain both positive and negative values "
    "around zero."
)

print(
    "The data generator adds random noise, so the observations "
    "do not lie exactly on the regression line."
)

print(
    "Heating costs are also limited below by zero using "
    "max(cost, 0)."
)

print(
    "For warm months this lower boundary may cause a systematic "
    "pattern in residuals because heating costs cannot become negative."
)

print(
    "Therefore, even a relatively high R^2 does not guarantee "
    "that the relationship is perfectly linear."
)


# ============================================================
# SIMPLE TEXT RESIDUAL GRAPH
# ============================================================

print("\nRESIDUAL GRAPH:")
print("Negative <---------- 0 ----------> Positive\n")

for month, residual in zip(months, residuals):

    position = int(round(residual * 5))

    left = 20
    width = 41

    line = [" "] * width
    line[left] = "|"

    point = left + position
    point = max(0, min(width - 1, point))

    line[point] = "*"

    print(
        f"{month:<4} "
        + "".join(line)
        + f" {residual:.3f}"
    )


# ============================================================
# TASK 4
# PREDICTION FOR -10 C
# ============================================================

print("\n" + "=" * 70)
print("TASK 4. PREDICTION AND EXTRAPOLATION")
print("=" * 70)

new_temperature = -10

prediction_minus_10 = (
    intercept
    + slope * new_temperature
)

min_temp = min(x)
max_temp = max(x)

print(
    f"\nObserved temperature range: "
    f"{min_temp} C to {max_temp} C"
)

print(
    f"Prediction temperature: "
    f"{new_temperature} C"
)

print(
    f"Predicted heating cost at -10 C = "
    f"{prediction_minus_10:.3f} thousand UAH"
)

if min_temp <= new_temperature <= max_temp:

    print("\nThis is interpolation.")

else:

    print("\nThis is extrapolation.")

    print(
        f"The minimum observed temperature is {min_temp} C, "
        f"while the prediction is made for {new_temperature} C."
    )

    print(
        "The prediction is less reliable because the model "
        "was not tested on temperatures outside the observed range."
    )


# ============================================================
# TASK 5
# REGRESSION AND CORRELATION
# ============================================================

print("\n" + "=" * 70)
print("TASK 5. REGRESSION AND CORRELATION")
print("=" * 70)

# t statistic for correlation / slope test
if abs(pearson_r) < 1:

    t_stat = (
        pearson_r
        * math.sqrt(
            (n - 2) /
            (1 - pearson_r ** 2)
        )
    )

else:
    t_stat = float("inf")


print(f"\nPearson r = {pearson_r:.6f}")
print(f"t-statistic = {t_stat:.6f}")
print(f"Degrees of freedom = {n - 2}")

print(
    "\nIn simple linear regression with one predictor, "
    "testing H0: slope = 0 and testing H0: correlation = 0 "
    "are equivalent tests."
)

print(
    "Therefore, scipy.stats.linregress() and pearsonr() "
    "produce the same or extremely close p-values "
    "for the same data."
)


# ============================================================
# CONTROL QUESTIONS
# ============================================================

print("\n" + "=" * 70)
print("CONTROL QUESTIONS")
print("=" * 70)

print("""
1. Why does least squares minimize squared residuals?

Squaring prevents positive and negative errors from cancelling
each other. Large errors also receive greater weight. This makes
it possible to find the regression line that best fits the data.


2. What does slope b1 mean?

The slope shows how much the predicted heating cost changes when
temperature increases by one degree Celsius.

Unlike correlation, slope has measurement units. Pearson r has
no units and only describes the strength and direction of the
linear relationship.


3. Why is high R^2 not enough?

R^2 shows the proportion of variation explained by the model,
but it does not show whether the relationship is truly linear.

Residual analysis can reveal curvature, unusual observations,
changing variance, or other systematic patterns.


4. What happens during extrapolation?

Extrapolation occurs when a prediction is made outside the
observed range of X values.

Such predictions are less reliable because the regression model
has not been tested on data outside the original range.
""")


# ============================================================
# FINAL RESULTS
# ============================================================

print("\n" + "=" * 70)
print("FINAL RESULTS")
print("=" * 70)

print(
    f"Regression equation: "
    f"cost = {intercept:.3f} "
    f"+ ({slope:.3f}) * temperature"
)

print(f"Pearson r = {pearson_r:.3f}")
print(f"R^2 = {r_squared:.3f}")

print(
    f"Prediction at -10 C = "
    f"{prediction_minus_10:.3f} thousand UAH"
)

print("\nPRACTICAL WORK 17 COMPLETED")
print("=" * 70)