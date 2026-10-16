import numpy as np
import pandas as pd

raw_data = [
    {"місто": "Київ", "ціна": 850, "кількість": 3.0},
    {"місто": "  Київ ", "ціна": "850 грн", "кількість": np.nan},
    {"місто": "КИЇВ", "ціна": 850, "кількість": 2.0},
    {"місто": "Київ", "ціна": "850 грн", "кількість": 3.0},
    {"місто": "Київ", "ціна": "850 грн", "кількість": 3.0},
    {"місто": "  Київ ", "ціна": 850, "кількість": np.nan},
    {"місто": "КИЇВ", "ціна": 7650, "кількість": 4.0},
    {"місто": "Київ", "ціна": 850, "кількість": 1.0}
]

df = pd.DataFrame(raw_data)

print(df)
print(df.isna().sum())

median_qty = df["кількість"].median()
df["кількість"] = df["кількість"].fillna(median_qty)

print(df)

print(df.duplicated())
print(df.duplicated(subset=["місто", "ціна", "кількість"]).sum())

df = df.drop_duplicates().reset_index(drop=True)
print(len(df))

df["ціна"] = df["ціна"].astype(str).str.replace(" грн", "").astype(float)
df["місто"] = df["місто"].str.strip().str.capitalize()

print(df["місто"].unique())
print(df.dtypes)
print(df)

q1 = df["ціна"].quantile(0.25)
q3 = df["ціна"].quantile(0.75)
iqr = q3 - q1
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr

print(q1, q3, iqr, lower_bound, upper_bound)
print(df[(df["ціна"] < lower_bound) | (df["ціна"] > upper_bound)])