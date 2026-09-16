import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

STUDENT_NAME = "Sender ilya"
STUDENT_GROUP = "IT-42"

city = "Суми"

months = np.arange(1, 13)
rain = np.array([40, 36, 33, 39, 52, 68, 75, 58, 42, 37, 42, 44])

print("Студент:", STUDENT_NAME)
print("Група:", STUDENT_GROUP)
print("Місто:", city)

print("\nЗавдання 1. Шкали вимірювання та міри центральної тенденції")

print("Місто — номінальна шкала")
print("Номер місяця — порядкова шкала")
print("Опади — шкала відношень")

print("Для міста використовується мода.")
print("Для номера місяця — медіана та мода.")
print("Для опадів — середнє, медіана та мода.")

print("\nЗавдання 2. Варіаційний ряд та частотний розподіл")

variation_series = np.sort(rain)

print("Варіаційний ряд:")
print(variation_series)

bins = [32, 43, 54, 65, 76]

intervals = pd.cut(
    rain,
    bins=bins,
    include_lowest=True
)

frequency = intervals.value_counts().sort_index()
relative_frequency = frequency / len(rain) * 100
cumulative_frequency = frequency.cumsum()

table = pd.DataFrame({
    "Частота": frequency,
    "Відносна частота (%)": relative_frequency.round(2),
    "Накопичена частота": cumulative_frequency
})

print("\nЧастотний розподіл:")
print(table)

print(
    "\nЧастка місяців з опадами до 65 мм:",
    cumulative_frequency.iloc[2] / len(rain) * 100,
    "%"
)

print("\nЗавдання 3. Побудова гістограм")

plt.hist(rain)
plt.xlabel("Кількість опадів, мм")
plt.ylabel("Частота")
plt.title("Розподіл опадів")
plt.show()

plt.hist(rain, bins=3)
plt.xlabel("Кількість опадів, мм")
plt.ylabel("Частота")
plt.title("Гістограма з 3 інтервалами")
plt.show()

plt.hist(rain, bins=10)
plt.xlabel("Кількість опадів, мм")
plt.ylabel("Частота")
plt.title("Гістограма з 10 інтервалами")
plt.show()

n = len(rain)

print("Кількість спостережень:", n)
print("Правило квадратного кореня:", np.sqrt(n))
print("Правило Стерджеса:", 1 + np.log2(n))

print("\nЗавдання 4. Статистичні характеристики")

mean = np.mean(rain)
median = np.median(rain)

values, counts = np.unique(rain, return_counts=True)
mode = values[np.argmax(counts)]

q1 = np.percentile(rain, 25)
q3 = np.percentile(rain, 75)

print("Середнє:", mean)
print("Медіана:", median)
print("Мода:", mode)
print("Q1:", q1)
print("Q3:", q3)

if mean > median:
    print("Розподіл має правосторонню асиметрію.")
elif mean < median:
    print("Розподіл має лівосторонню асиметрію.")
else:
    print("Розподіл приблизно симетричний.")

print("\nЗавдання 5. Висновки")

print("1. Середнє для міста використовувати недоцільно,")
print("оскільки місто є номінальною ознакою.")

print("2. Номер місяця має природний порядок,")
print("тому його можна розглядати як порядкову шкалу.")

print("3. Для кількості опадів можна використовувати")
print("середнє, медіану та моду.")

print("4. Гістограма показує розподіл кількості опадів")
print("за певними інтервалами.")

print("5. Накопичена частота показує кількість спостережень,")
print("які не перевищують верхню межу відповідного інтервалу.")
