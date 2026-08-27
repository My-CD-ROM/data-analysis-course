#Завдання 1. Створення масивів

import numpy as np

temps = np.array([-3, -2, 2, 8, 13, 16, 18, 17, 13, 8, 3, -1])
days_in_month = np.array([31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31])
month_numbers = np.arange(1, 13)

def shape_dtype(x, y, z):
    """shape та dtype 3-х масивів"""
    print(f"temps shape: {x.shape}, dtype: {x.dtype}")
    print(f"days_in_month shape: {y.shape}, dtype: {y.dtype}")
    print(f"month_numbers shape: {z.shape}, dtype: {z.dtype}")

shape_dtype(temps, days_in_month, month_numbers)

print("______________________________________")

#Завдання 2. Векторизовані обчислення

tempsF = temps * 9 / 5 + 32
print(f"Темпр у F: {tempsF}")

warm_days = days_in_month[temps > 15]
total_warm_days = warm_days.sum()

print(f"теплi дні: {total_warm_days}")
print(f" 365 днів: {days_in_month.sum() == 365}")

sum_days = sum(days_in_month)
print(f"Сума днів: {sum_days}")

print("______________________________________")
#Завдання 3. Індексація і фільтрація

value_max = temps[0]
index_max = 0

value_min = temps[0]
index_min = 0

for i, el in enumerate(temps.flat):
    if el > value_max:
        value_max = el
        index_max= i
        
    if el < value_min:
        value_min = el
        index_min = i 

print(f"max: { value_max } --- min: { value_min } ")
print("index max: ", index_max, "index min: ",index_min )

#2
cmonths = month_numbers[temps < 0]

print(f"нижче 0 C: {cmonths}")

#3
a = np.empty(12)
np.copyto(a, temps)
print(np.sort(a))

print("______________________________________")
#Завдання 4. Двовимірний масив і axis
#1
random = np.array([ 55, 70, 100, 130, 170, 190,
                    220, 210, 160, 120, 70, 50])

data = np.array([temps, days_in_month, random])

print(data)
print("shape:", data.shape)
#2
rsum = data.sum(axis=1)
rons = data.mean(axis=1)

print("Суми:", rsum)
print("Середні:", rons)

#3

csums = data.sum(axis=0)

print("по стовпцях:", csums)

print("______________________________________")
#Завдання 5. reshape і broadcasting

rows = np.array([temps, days_in_month])

print("rows:")
print(rows)
print("shape:", rows.shape)
print("______")
correction = np.array([1, 0])

print("correction:", correction)
print("shape:", correction.shape)
print("______")

# rows + correction
# форми (2, 12) і (2,) несумісні

correction = correction.reshape(2, 1)

print("correction після reshape:")
print(correction)
print("shape:", correction.shape)

result = rows + correction

print("Результат:")
print(result)
