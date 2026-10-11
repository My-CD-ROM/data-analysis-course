import pandas as pd

months = ["Січ", "Лют", "Бер", "Кві", "Тра", "Чер",
	  "Лип", "Сер", "Вер", "Жов", "Лис", "Гру"]
avg_temp = [-4, -3, 2, 9, 15, 19, 21, 20, 14, 8, 2, -2]
precip = [38, 36, 38, 41, 53, 74, 84, 69, 47, 36, 44, 44]

df = pd.DataFrame({
    "month": months,
    "avg_temp": avg_temp,
    "precip": precip
})

print("--- df.head() ---")
print(df.head())

print("\n--- df.shape ---")
print(df.shape)

print("\n--- df.dtypes ---")
print(df.dtypes)

print("\nЗавдання 1. Індекс\n")

print(df.index)
df.set_index("month", inplace=True)
print(df.loc["Сер"])
print(df.head())


print("\nЗавдання 2. Відбір рядків і стовпців\n")

df.reset_index(inplace=True)
df.index = range(1,13)
print(df.loc[1:6, "avg_temp"])
print(df.iloc[0:6, 1])
print(df[["month", "precip"]])

print("\nЗавдання 3. Фільтрація за умовою\n")

print(df[df["avg_temp"] > 15])
print(df[(df["avg_temp"] > 10) & (df["precip"] > 50)])
print(df[(df["avg_temp"] < 0) | (df["precip"] > 80)])

print("\nЗавдання 4. Обчислювані стовпці\n")

df["avg_temp_f"] = df["avg_temp"] * 9 / 5 + 32

df["is_wet"] = df["precip"] > df["precip"].mean()

def get_season(m):
    if m in [12, 1, 2]:
        return "зима"
    elif m in [3, 4, 5]:
        return "весна"
    elif m in [6, 7, 8]:
        return "літо"
    else:
        return "осінь"

df["season"] = df.index.to_series().apply(get_season) 
print(df)
