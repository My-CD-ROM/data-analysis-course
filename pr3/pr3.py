import pandas as pd

wide_df = pd.DataFrame({
    "місто": ["Київ"],
    "Січ": [78], "Лют": [74], "Бер": [68], "Кві": [58],
    "Тра": [50], "Чер": [44], "Лип": [40], "Сер": [42],
    "Вер": [52], "Жов": [66], "Лис": [76], "Гру": [82]
})

print(wide_df)
print(wide_df.shape)

tidy_df = wide_df.melt(
    id_vars="місто",
    var_name="місяць",
    value_name="хмарність"
)

print(tidy_df)
print(tidy_df.shape)

back_wide = tidy_df.pivot(
    index="місто",
    columns="місяць",
    values="хмарність"
).reset_index()

month_order = ["місто"] + list(wide_df.columns[1:])
back_wide = back_wide[month_order]

print(back_wide)
print(wide_df.equals(back_wide))

tidy_df.to_csv("variant.csv", index=False)
tidy_df.to_json("variant.json", orient="records", force_ascii=False)

reloaded_csv = pd.read_csv("variant.csv")
reloaded_json = pd.read_json("variant.json")

print(reloaded_csv)
print(reloaded_json)

print(open("variant.csv", encoding="utf-8").read())
print(open("variant.json", encoding="utf-8").read())