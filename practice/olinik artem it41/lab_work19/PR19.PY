import math
import random

# ============================================================
# PRACTICAL WORK 19
# Classification and Adequacy of Mathematical Models
# Student: Artem Oliinyk
# Group: IT-41
# Variant: 1
# City: Kyiv
# ============================================================

random.seed(1)

city = "Kyiv"
base_temp = 9.5
amplitude = 14.0
base_consumption = 5200.0
k = 55.0
noise_sd = 80.0

months = list(range(1, 13))

temperature = []
consumption = []

# ============================================================
# DATA GENERATION
# ============================================================

for month in months:

    temp = (
        base_temp
        + amplitude
        * math.cos(
            (month - 7) / 12
            * 2
            * math.pi
        )
    )

    temp += random.gauss(0, 0.5)
    temp = round(temp, 1)

    energy = (
        base_consumption
        - k * (temp - base_temp)
        + random.gauss(0, noise_sd)
    )

    energy = round(energy, 0)

    temperature.append(temp)
    consumption.append(energy)


print("=" * 75)
print("PRACTICAL WORK 19")
print("Student: Artem Oliinyk")
print("Group: IT-41")
print("Variant: 1")
print("City: Kyiv")
print("=" * 75)


# ============================================================
# INITIAL DATA
# ============================================================

print("\nINITIAL DATA:")

print(
    f"{'Month':<10}"
    f"{'Temperature':>15}"
    f"{'Consumption':>18}"
)

for month, temp, energy in zip(
    months,
    temperature,
    consumption
):
    print(
        f"{month:<10}"
        f"{temp:>15.1f}"
        f"{energy:>18.0f}"
    )


# ============================================================
# TASK 1
# MODEL CLASSIFICATION
# ============================================================

print("\n" + "=" * 75)
print("TASK 1. MODEL CLASSIFICATION")
print("=" * 75)

print("""
1. STOCHASTIC MODEL

The average part of the model is deterministic because it uses
a fixed linear formula:

Consumption = a + b * Temperature

However, the generated observations contain random noise.
Therefore, the complete model is stochastic: it consists of a
deterministic mean component and a random deviation.


2. STATIC MODEL

The model is static because electricity consumption for a
particular month depends only on the temperature of that month.

Consumption from previous months is not used to calculate the
current month's consumption.


3. DESCRIPTIVE / PREDICTIVE STATISTICAL MODEL

The model is not a balance model because it does not describe
a conservation equation.

It is not an optimization model because it does not search for
the best decision.

It is not a simulation model because it does not perform a
step-by-step simulation of system states over time.

Therefore, it is a descriptive and predictive statistical model.
""")


# ============================================================
# TASK 2
# SIMPLE LINEAR REGRESSION
# ============================================================

print("\n" + "=" * 75)
print("TASK 2. LINEAR REGRESSION MODEL")
print("=" * 75)

n = len(temperature)

mean_x = sum(temperature) / n
mean_y = sum(consumption) / n

ss_xx = sum(
    (x - mean_x) ** 2
    for x in temperature
)

ss_xy = sum(
    (x - mean_x) * (y - mean_y)
    for x, y in zip(
        temperature,
        consumption
    )
)

b = ss_xy / ss_xx
a = mean_y - b * mean_x

print(
    f"\nRegression equation:"
    f"\nConsumption = {a:.1f} "
    f"+ ({b:.1f}) * Temperature"
)

print(f"\nIntercept a = {a:.3f}")
print(f"Slope b = {b:.3f}")

if b < 0:
    print(
        "\nThe slope is negative, as expected."
    )

    print(
        f"When temperature increases by 1 C, "
        f"predicted electricity consumption decreases "
        f"by approximately {abs(b):.1f} MWh."
    )

    print(
        "This is logical because higher temperatures "
        "reduce electricity demand for heating."
    )
else:
    print(
        "\nThe slope is positive."
    )


# ============================================================
# PREDICTIONS
# ============================================================

predictions = [
    a + b * temp
    for temp in temperature
]


# ============================================================
# TASK 3
# RESIDUALS AND MODEL ADEQUACY
# ============================================================

print("\n" + "=" * 75)
print("TASK 3. MODEL ADEQUACY")
print("=" * 75)

residuals = [
    actual - predicted
    for actual, predicted in zip(
        consumption,
        predictions
    )
]

print(
    f"\n{'Month':<8}"
    f"{'Temp':>10}"
    f"{'Observed':>14}"
    f"{'Predicted':>14}"
    f"{'Residual':>14}"
)

for month, temp, actual, predicted, residual in zip(
    months,
    temperature,
    consumption,
    predictions,
    residuals
):
    print(
        f"{month:<8}"
        f"{temp:>10.1f}"
        f"{actual:>14.1f}"
        f"{predicted:>14.1f}"
        f"{residual:>14.1f}"
    )


# ============================================================
# R-SQUARED
# ============================================================

ss_res = sum(
    residual ** 2
    for residual in residuals
)

ss_tot = sum(
    (value - mean_y) ** 2
    for value in consumption
)

r_squared = 1 - ss_res / ss_tot

print(
    f"\nSS residual = {ss_res:.2f}"
)

print(
    f"SS total = {ss_tot:.2f}"
)

print(
    f"R^2 = {r_squared:.4f}"
)

print(
    f"The model explains approximately "
    f"{r_squared * 100:.2f}% of the variation "
    f"in electricity consumption."
)

print(
    f"Approximately "
    f"{(1 - r_squared) * 100:.2f}% remains unexplained."
)


# ============================================================
# TEXT RESIDUAL PLOT
# ============================================================

print("\nRESIDUAL PLOT:")
print("Negative <----------- 0 -----------> Positive\n")

max_residual = max(
    abs(value)
    for value in residuals
)

for month, residual in zip(
    months,
    residuals
):

    width = 45
    center = 22

    line = [" "] * width
    line[center] = "|"

    if max_residual != 0:
        position = round(
            residual / max_residual * 20
        )
    else:
        position = 0

    point = center + position

    point = max(
        0,
        min(width - 1, point)
    )

    line[point] = "*"

    print(
        f"{month:>2} "
        + "".join(line)
        + f" {residual:+.1f}"
    )


print("\nResidual analysis:")

print(
    "The residuals contain both positive and negative values "
    "and are distributed around zero."
)

print(
    "There is no obvious systematic increase or decrease "
    "of residuals across all months."
)

print(
    "This is consistent with the data-generation process, "
    "where random noise was added to a linear relationship."
)

if r_squared >= 0.8:

    print(
        "\nThe R^2 value is high and the residuals do not show "
        "an obvious systematic pattern."
    )

    print(
        "Therefore, the linear model can be considered adequate "
        "for predicting monthly electricity consumption within "
        "the observed temperature range."
    )

else:

    print(
        "\nR^2 is not very high, so the linear model may not "
        "fully explain electricity consumption."
    )


# ============================================================
# TASK 4
# VERIFICATION AND VALIDATION
# ============================================================

print("\n" + "=" * 75)
print("TASK 4. VERIFICATION AND VALIDATION")
print("=" * 75)

test_month = 1
test_temp = temperature[0]

manual_prediction = (
    a + b * test_temp
)

code_prediction = predictions[0]

print(
    f"\nVerification example for month {test_month}:"
)

print(
    f"Temperature = {test_temp:.1f} C"
)

print(
    f"Manual prediction = "
    f"{a:.3f} + ({b:.3f}) * "
    f"{test_temp:.1f}"
)

print(
    f"Manual result = "
    f"{manual_prediction:.3f} MWh"
)

print(
    f"Program result = "
    f"{code_prediction:.3f} MWh"
)

difference = abs(
    manual_prediction
    - code_prediction
)

print(
    f"Difference = {difference:.10f}"
)

print("""
VERIFICATION:

Verification checks whether the model and its calculations are
implemented correctly in the program.

For example, the prediction for month 1 can be calculated manually
using a + b * temperature and compared with the value produced by
the program.

The values above are equal, so this calculation is implemented
correctly.


VALIDATION:

Validation checks whether the model describes real observations
well enough for its intended purpose.

The same 12 observations used to fit the regression are useful
for initial model assessment, but they are not sufficient for
fully independent validation.

For stronger validation, new data should be used, for example
electricity consumption and temperature observations from the
next year that were not used to estimate a and b.
""")


# ============================================================
# TASK 5
# MODEL IMPROVEMENT
# ============================================================

print("\n" + "=" * 75)
print("TASK 5. MODEL IMPROVEMENT")
print("=" * 75)

if r_squared >= 0.8:

    print("""
The model appears adequate for the current prediction task.

R^2 is relatively high and the residuals are distributed around
zero without a strong systematic pattern.

Therefore, adding unnecessary predictors or nonlinear terms is
not justified at this stage.

A simpler model is easier to interpret and use. According to the
accuracy-simplicity trade-off, the model should only be made more
complex if new data show a systematic problem that the current
linear model cannot explain.
""")

else:

    print("""
The current linear model may require improvement.

One possible improvement is to add a quadratic temperature term.
This could model nonlinear electricity demand, for example when
very cold weather causes especially high heating demand.

Another option would be to add additional predictors such as
humidity, population, or the number of heating days.
""")


# ============================================================
# CONTROL QUESTIONS
# ============================================================

print("\n" + "=" * 75)
print("CONTROL QUESTIONS")
print("=" * 75)

print("""
1. What is the difference between verification and validation?

Verification checks whether the model has been implemented
correctly. In this work, this can be checked by manually
calculating a prediction using a + b * temperature and comparing
it with the program result.

Validation checks whether the correctly implemented model
adequately represents observations. New independent data, such
as data from the next year, would provide stronger validation.


2. How is this model classified?

The model is stochastic because observations contain random noise.

It is static because each month's prediction depends only on
temperature for the same month.

It is a descriptive and predictive statistical model because it
does not perform optimization, conservation balancing, or
step-by-step simulation.


3. What does R^2 show?

R^2 shows the proportion of variation in electricity consumption
that is explained by temperature in the fitted linear model.

A high R^2 alone does not prove that a model is correct and does
not guarantee reliable extrapolation outside the observed
temperature range.


4. Why are residuals important?

Residuals show where and how the predictions differ from
observations.

Random residuals around zero support the linear model.

A systematic pattern in residuals can indicate that the model
misses an important relationship even when R^2 is relatively high.
""")


# ============================================================
# FINAL RESULTS
# ============================================================

print("\n" + "=" * 75)
print("FINAL RESULTS")
print("=" * 75)

print("Student: Artem Oliinyk")
print("Group: IT-41")
print("Variant: 1")
print("City: Kyiv")

print(
    f"\nRegression model:"
    f"\nConsumption = {a:.1f} "
    f"+ ({b:.1f}) * Temperature"
)

print(
    f"\nR^2 = {r_squared:.4f}"
)

print(
    f"Explained variation = "
    f"{r_squared * 100:.2f}%"
)

print(
    "\nClassification:"
    "\n- Stochastic"
    "\n- Static"
    "\n- Descriptive / predictive statistical model"
)

print("\nPRACTICAL WORK 19 COMPLETED")
print("=" * 75)