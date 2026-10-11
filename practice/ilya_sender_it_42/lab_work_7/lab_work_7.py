import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

np.random.seed(9)

city = "Суми"
base_sales = 31
base_temperature = -1

days = np.arange(1, 31)

weekend = (days % 7 == 6) | (days % 7 == 0)

temperature = base_temperature + np.random.uniform(-3, 3, 30)

sales = base_sales + np.random.randint(-5, 6, 30)

sales = sales.astype(float)
sales[weekend] *= np.random.uniform(1.15, 1.25, weekend.sum())
sales = np.round(sales).astype(int)

data = pd.DataFrame({
    "день": days,
    "вихідний": weekend,
    "температура": np.round(temperature, 1),
    "продажі": sales
})

print("Варіант 9")
print("Місто:", city)
print("Базові продажі:", base_sales)
print("Середня температура:", base_temperature)
print()
print(data)


print("\nЗавдання 1. Побудова власного набору")

print(data)


print("\nЗавдання 2. Гістограма")

fig, ax = plt.subplots(figsize=(6, 4))

ax.hist(data["продажі"], bins=5, edgecolor="black")

ax.set_xlabel("Продажі, шт./день")
ax.set_ylabel("Кількість днів")
ax.set_title("Розподіл продажів у Сумах за 30 днів")

plt.show()


fig, ax = plt.subplots(figsize=(6, 4))

ax.hist(data["продажі"], bins=10, edgecolor="black")

ax.set_xlabel("Продажі, шт./день")
ax.set_ylabel("Кількість днів")
ax.set_title("Розподіл продажів у Сумах за 30 днів — 10 інтервалів")

plt.show()

print("Для 30 значень більш зрозумілою є гістограма з 5 інтервалами,")
print("оскільки вона показує загальну форму розподілу без зайвої деталізації.")


print("\nЗавдання 3. Boxplot")

weekday_sales = data.loc[~data["вихідний"], "продажі"]
weekend_sales = data.loc[data["вихідний"], "продажі"]

fig, ax = plt.subplots(figsize=(6, 4))

ax.boxplot(
    [weekday_sales, weekend_sales],
    labels=["Будні", "Вихідні"]
)

ax.set_ylabel("Продажі, шт./день")
ax.set_title("Продажі у будні та вихідні")

plt.show()

print("Медіана та розкид продажів у вихідні вищі,")
print("оскільки у вихідні продажі були задані на 15–25% більшими.")


print("\nЗавдання 4. Діаграма розсіювання")

fig, ax = plt.subplots(figsize=(6, 4))

ax.scatter(
    data["температура"],
    data["продажі"]
)

ax.set_xlabel("Температура, °C")
ax.set_ylabel("Продажі, шт./день")
ax.set_title("Продажі залежно від температури")

plt.show()

print("На графіку видно залежність продажів від температури.")
print("Для цього набору даних зв'язок може бути слабким,")
print("оскільки продажі формувалися також із випадковою варіацією")
print("та підвищенням у вихідні дні.")


print("\nЗавдання 5. Навмисно спотворений графік")

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

axes[0].hist(data["продажі"], bins=5, edgecolor="black")
axes[0].set_xlabel("Продажі, шт./день")
axes[0].set_ylabel("Кількість днів")
axes[0].set_title("Коректна гістограма")

axes[1].hist(data["продажі"], bins=5, edgecolor="black")
axes[1].set_xlabel("Продажі, шт./день")
axes[1].set_ylabel("Кількість днів")
axes[1].set_title("Спотворена гістограма")

axes[1].set_ylim(0, 2)

plt.tight_layout()
plt.show()

print("У спотвореному графіку вісь Y обрізана.")
print("Через це стовпці візуально виглядають значно вищими,")
print("а різниця між ними сприймається сильніше.")
print("Це приклад спотворення масштабу осі.")


print("\nКонтрольні питання")

print("\n1. Чому обрізана вісь Y перебільшує різницю?")
print("Якщо початкова точка осі Y змінена або масштаб сильно обрізаний,")
print("невелика числова різниця може виглядати значною на графіку.")

print("\n2. Коли лінійний графік є помилкою?")
print("Наприклад, для категорій 'чай', 'кава', 'сік'.")
print("З'єднання таких категорій лінією створює враження,")
print("що між ними існує певна числова послідовність.")

print("\n3. Чому важливі підписи осей та одиниці?")
print("Вони пояснюють, що саме вимірюється та в яких одиницях.")
print("Без них графік може бути неправильно інтерпретований.")

print("\n4. Що таке chartjunk?")
print("Chartjunk — це зайві графічні елементи, які не передають дані.")
print("Наприклад, непотрібний 3D-ефект може ускладнювати")
print("порівняння значень замість того, щоб допомагати його.")
