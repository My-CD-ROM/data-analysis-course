import numpy as np

# 1. Підготовка даних (визначено масиви на 12 місяців для сумісності розмірностей)
temps = np.array([-4, -3, 2, 9, 15, 20, 22, 21, 15, 9, 3, -2])
days_in_month = np.array([31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])
month_numbers = np.arange(1, 13)

print("Форма temps:", temps.shape)
print( temps.dtype)

# Конвертація у Фаренгейти
temps_f = temps * 9/5 + 32
print("Температури у Фаренгейтах:", temps_f)

# Розрахунок кількості днів з температурою > 15°C
# (виправлено: days_in_month тепер масив, а не одне число)
total_days = days_in_month[temps > 15].sum()
print(f"Всього днів у році тепліше 15°C: {total_days}")

# Пошук екстремумів
max_temp = temps.max()
max_index = temps.argmax()
min_temp = temps.min()
min_index = temps.argmin()

print(f"Найтепліший місяць: значення {max_temp}°C, індекс {max_index}")
print(f"Найхолодніший місяць: значення {min_temp}°C, індекс {min_index}")

# Булева індексація
below_zero_mask = temps < 0
cold_months = month_numbers[below_zero_mask]
print("Номери місяців з температурою нижче нуля:", cold_months)

# Сортування
sorted_temps = np.sort(temps)
print("Відсортовані температури:", sorted_temps)

# 2. Об'єднання у двовимірний масив форми (3, 12)
sunshine_hours = np.array([40, 60, 110, 160, 240, 270, 290, 250, 170, 100, 50, 35])
data_matrix = np.vstack((temps, days_in_month, sunshine_hours))

row_sums = data_matrix.sum(axis=1)
row_means = data_matrix.mean(axis=1)
col_sums = data_matrix.sum(axis=0)

print("\nСуми по рядках:", row_sums)
print("Середні по рядках:", np.round(row_means, 2))
print("Суми по стовпцях:", col_sums)

# 3. Трансляція (Broadcasting)
# (виправлено: додано визначення змінних rows та correction)
rows = np.vstack((temps, days_in_month))
correction = np.array([1, 0])

correction_reshaped = correction.reshape(2, 1)
result = rows + correction_reshaped

print("\nРезультат додавання поправки до rows:")
print(result)