import pandas as pd

months = ["Січ", "Лют", "Бер", "Кві", "Тра", "Чер", "Лип", "Сер", "Вер", "Жов", "Лис", "Гру"]

avg_temp = [-4, -3, 2, 9, 15, 20, 22, 21, 15, 9, 3, -2]
precip = [38, 36, 38, 41, 53, 74, 84, 69, 47, 36, 44, 44]

df = pd.DataFrame({
    "month": months,
    "avg_temp": avg_temp,
    "precip": precip
})

print("=== КРОК 1. Побудова DataFrame ===")
print("Перші рядки таблиці (df.head()):")
print(df.head())
print("\nФорма таблиці (df.shape):", df.shape)
print("\nТипи даних стовпців (df.dtypes):")
print(df.dtypes)
print("=" * 60)

print("\n=== ЗАВДАННЯ 1. Індекс ===")

print("1. Індекс за замовчуванням:", df.index)

df_by_month = df.set_index("month")
print("\n2. Рядок для місяця 'Тра' через .loc:")
print(df_by_month.loc["Тра"])

df = df_by_month.reset_index()
print("\n3. Відновлений DataFrame зі звичайним індексом:")
print(df.head(3))
print("=" * 60)


print("\n=== ЗАВДАННЯ 2. Відбір рядків і стовпців ===")


df.index = range(1, 13)

print("1. Стовпець avg_temp для підписів від 1 до 6 включно (.loc[1:6]):")
print(df.loc[1:6, "avg_temp"])

print("\n2. Стовпець avg_temp за позиціями 0..5 (.iloc[0:6, 1]):")
print(df.iloc[0:6, 1])

print("\n3. Стовпці 'month' та 'precip' для всіх рядків:")
print(df[["month", "precip"]])
print("=" * 60)

print("\n=== ЗАВДАННЯ 3. Фільтрація за умовою ===")

print("1. Місяці з температурою avg_temp > 15:")
print(df[df["avg_temp"] > 15])

print("\n2. Місяці, де avg_temp > 10 ТА precip > 50:")
print(df[(df["avg_temp"] > 10) & (df["precip"] > 50)])

print("\n3. Місяці, де avg_temp < 0 АБО precip > 80:")
print(df[(df["avg_temp"] < 0) | (df["precip"] > 80)])
print("=" * 60)

print("\n=== ЗАВДАННЯ 4. Обчислювані стовпці ===")

df["avg_temp_f"] = df["avg_temp"] * 9 / 5 + 32

df["is_wet"] = df["precip"] > df["precip"].mean()

def get_season(month_num):
    if month_num in [12, 1, 2]:
        return "зима"
    elif month_num in [3, 4, 5]:
        return "весна"
    elif month_num in [6, 7, 8]:
        return "літо"
    else:
        return "осінь"

df["season"] = pd.Series(df.index).apply(get_season).values

print("Підсумкова таблиця з усіма обчислюваними стовпцями:")
print(df)
print("=" * 60)