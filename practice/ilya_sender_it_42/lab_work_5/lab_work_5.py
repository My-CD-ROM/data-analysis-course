import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

months = np.arange(1, 13)

rain = np.array([
    40, 36, 33, 39, 52, 68,
    75, 58, 42, 37, 42, 44
])


# Завдання 1

print("ЗАВДАННЯ 1")
print()

print("Місто — номінальна шкала.")
print("Місяці — порядкова шкала (можна аргументувати як інтервальну).")
print("Кількість опадів — відносна шкала.")
print()

print("Для міста коректна міра положення: мода.")
print("Для номера місяця коректна міра: медіана, мода.")
print("Для кількості опадів коректні: середнє, медіана, мода.")
print()


# Завдання 2

print("ЗАВДАННЯ 2")
print()

variation_series = np.sort(rain)

print("Варіаційний ряд:")
print(variation_series)
print()


# 4 інтервали
# Мінімум = 33
# Максимум = 75
#
# Обираємо приблизно рівні інтервали:
# 33–43
# 44–54
# 55–65
# 66–76

bins = [32, 43, 54, 65, 76]

intervals = pd.cut(rain,bins=bins,include_lowest=True)
freq = intervals.value_counts().sort_index()

relative_freq = freq / len(rain) * 100

cumulative_freq = freq.cumsum()

frequency_table = pd.DataFrame({
    "абсолютна": freq,
    "відносна_%": relative_freq.round(2),
    "накопичена": cumulative_freq
})

print("Частотна таблиця:")
print(frequency_table)
print()


print("Частка місяців із кількістю опадів не більше межі третього інтервалу:")

third_interval_cumulative = cumulative_freq.iloc[2]

print(
    third_interval_cumulative,
    "із",
    len(rain),
    "місяців"
)

print(
    third_interval_cumulative / len(rain) * 100,
    "%"
)

print()

# Завдання 3

print("ЗАВДАННЯ 3")
print()

# 1. Гістограма з кількістю bins за замовчуванням
plt.hist(rain, edgecolor="black")
plt.title("Опади за замовчуванням")
plt.xlabel("Кількість опадів, мм")
plt.ylabel("Кількість місяців")
plt.show()


# 2. Гістограма з 3 інтервалами
plt.hist(rain, bins=3, edgecolor="black")
plt.title("Опади — 3 інтервали")
plt.xlabel("Кількість опадів, мм")
plt.ylabel("Кількість місяців")
plt.show()


# Гістограма з 10 інтервалами
plt.hist(rain, bins=10, edgecolor="black")
plt.title("Опади — 10 інтервалів")
plt.xlabel("Кількість опадів, мм")
plt.ylabel("Кількість місяців")
plt.show()


# Правило sqrt(n)
n = len(rain)
sqrt_bins = np.sqrt(n)

# Правило Стерджеса
sturges_bins = 1 + np.log2(n)

print("Кількість спостережень:", n)
print("Правило √n:", sqrt_bins)
print("Правило Стерджеса:", sturges_bins)
print()

print(
    "Орієнтовно для 12 спостережень доцільно використовувати "
    "близько 3–4 інтервалів."
)

print(
    "Для цього набору гістограма з 3 інтервалами є достатньо "
    "зрозумілою, оскільки 12 значень — дуже невеликий набір.")

# Завдання 4

print("ЗАВДАННЯ 4")
print()

mean = rain.mean()
median = np.median(rain)
mode = pd.Series(rain).mode()

q1 = np.quantile(rain, 0.25)
q3 = np.quantile(rain, 0.75)

print("Середнє:", mean)
print("Медіана:", median)
print("Мода:", mode.values)

print("Q1:", q1)
print("Q3:", q3)

print()

print("Порівняння середнього і медіани:")

if mean > median:
    print("Середнє більше за медіану. " "Це свідчить про певну правосторонню асиметрію.")
elif mean < median:
    print(
        "Середнє менше за медіану. "
        "Це свідчить про певну лівосторонню асиметрію."
    )
else:
    print("Середнє і медіана однакові.")

print()


# Завдання 5

print("ЗАВДАННЯ 5")
print()

print(
    "Кількість опадів належить до відносної шкали, "
    "оскільки має природний нуль: 0 мм означає повну "
    "відсутність опадів. Тому для неї мають зміст "
    "середнє, медіана і мода."
)

print()

print(
    "Місто належить до номінальної шкали. Назви міст "
    "є категоріями, між якими немає числового порядку. "
    "Тому для міста можна використовувати лише моду."
)

print()

print("2")
print(
    "Місяці мають природний порядок, але нульового місяця "
    "не існує. Тому номер місяця можна розглядати як "
    "порядкову шкалу. Водночас календарні проміжки між "
    "послідовними номерами однакові, тому можна навести "
    "аргумент на користь інтервальної шкали."
)

print()

print("3")
print(
    "Кількість опадів — числова змінна, а більшість її "
    "значень різні. Стовпчикова діаграма для кожного "
    "окремого значення була б малозмістовною. Гістограма "
    "об'єднує значення в інтервали і показує форму розподілу."
)

print()

print("4")
print(
    "Накопичена частота показує кількість спостережень, "
    "які не перевищують верхню межу відповідного інтервалу.")
