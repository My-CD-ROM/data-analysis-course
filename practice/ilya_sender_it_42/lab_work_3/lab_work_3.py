import pandas as pd

print("Завдання 1. Побудова wide-таблиці свого варіанта\n")

wide = pd.DataFrame({
    "місто": ["Київ"],
    "Січ": [78], "Лют": [74], "Бер": [68], "Кві": [58],
    "Тра": [50], "Чер": [44], "Лип": [40], "Сер": [42],
    "Вер": [52], "Жов": [66], "Лис": [76], "Гру": [82]
})

print(wide)

print("\nЗавдання 2. Приведення до tidy (melt)\n")

tidy = wide.melt(id_vars="місто", var_name="місяць", value_name="хмарність")
print(tidy)

print("shape:", tidy.shape)

print("\nЗавдання 3. Класифікація змінних \n")

#місто це номінальна шкала бо назва міста це текстова категорія
#вона без порядку чи арифметичних властивостей.

#місяць це порядкова шкала бо значення мають 
#чітку часову послідовність.

#хмарність це шкала відношень бо числова змінна з 
#рівними інтервалами та абсолютним нулем 
print("\nЗавдання 4. Зворотне перетворення й перевірка\n")

pivot = tidy.pivot(index="місто", columns="місяць", values="хмарність").reset_index()
months_order = ["місто", "Січ", "Лют", "Бер", "Кві", "Тра", "Чер", "Лип", "Сер", "Вер", "Жов", "Лис", "Гру"]
pivot = pivot[months_order]

print(pivot)
print("Значення:", wide.equals(pivot))

print("\nЗавдання 5. Читання й запис (CSV та JSON)\n")

tidy.to_csv("variant.csv", index=False)
tidy.to_json("variant.json", orient="records", force_ascii=False)

reloaded_csv = pd.read_csv("variant.csv")
reloaded_json = pd.read_json("variant.json")
print("csv")
print(open("variant.csv", encoding="utf-8").read())
print("json")
print(open("variant.json", encoding="utf-8").read())
