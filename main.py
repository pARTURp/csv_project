import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# ==== Настройки ====
CSV_PATH = "vancouver_age.csv"
OUT_DIR = "simple_analysis_outputs"
os.makedirs(OUT_DIR, exist_ok=True)

# ==== Загрузка и очистка данных ====
df = pd.read_csv(CSV_PATH, encoding="utf-8-sig")
df.columns = df.columns.str.strip()
df["Variable"] = df["Variable"].astype(str).str.strip()
area_cols = [c for c in df.columns if c not in ("ID", "Variable")]

# Очистка чисел
for c in area_cols:
    df[c] = (
        df[c]
        .astype(str)
        .str.replace(r"[^\d\.-]", "", regex=True)
        .replace("", "0")
    )
    df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0).astype(int)

# ==== Функция для суммирования по шаблону Variable ====
def get_series_by_pattern(pattern_regex):
    mask = df["Variable"].str.contains(pattern_regex, regex=True, na=False)
    sel = df.loc[mask, area_cols]
    if sel.shape[0] == 0:
        return pd.Series(0, index=area_cols)
    return sel.sum(axis=0)

# ==== 1️⃣ Больше всего пожилых (65+) ====
elderly = get_series_by_pattern(r"65 years and over")
top_elderly = elderly.idxmax()
print(f"🏥 Больше всего пожилых: {top_elderly}")

plt.figure(figsize=(10,5))
elderly.sort_values(ascending=True).plot(kind="barh", color="salmon")
plt.title("Численность пожилых жителей по районам (65+)")
plt.xlabel("Численность")
plt.ylabel("Район")
plt.tight_layout()
plt.show()

# ==== 2️⃣ Средний возраст ====
avg_age = df.loc[df["Variable"].str.contains("Average age of the population"), area_cols].squeeze()
median_age = avg_age.median()
younger_than_median = avg_age[avg_age < median_age].sort_values()
older_than_median = avg_age[avg_age > median_age].sort_values()
print(f"📊 Районы с ниже среднего возраста: {list(younger_than_median.index)}")
print(f"📊 Районы с выше среднего возраста: {list(older_than_median.index)}")

plt.figure(figsize=(10,5))
avg_age.sort_values().plot(kind="barh", color="skyblue")
plt.title("Средний возраст по районам")
plt.xlabel("Средний возраст")
plt.ylabel("Район")
plt.tight_layout()
plt.show()

# ==== 3️⃣ Больше всего подростков (15–19) ====
teenagers = get_series_by_pattern(r"15 to 19")
top_teen = teenagers.idxmax()
print(f"👦 Больше всего подростков: {top_teen}")

plt.figure(figsize=(10,5))
teenagers.sort_values(ascending=True).plot(kind="barh", color="orange")
plt.title("Численность подростков (15–19) по районам")
plt.xlabel("Численность")
plt.ylabel("Район")
plt.tight_layout()
plt.show()

# ==== 4️⃣ Больше всего детей (0–14) ====
children = get_series_by_pattern(r"0 to 4|5 to 9|10 to 14")
top_children = children.idxmax()
print(f"🧒 Больше всего детей: {top_children}")

plt.figure(figsize=(10,5))
children.sort_values(ascending=True).plot(kind="barh", color="green")
plt.title("Численность детей (0–14) по районам")
plt.xlabel("Численность")
plt.ylabel("Район")
plt.tight_layout()
plt.show()

# ==== 5️⃣ Район с наиболее равномерным распределением возрастов ====
age_groups_pattern = r"0 to 4|5 to 9|10 to 14|15 to 19|20 to 24|25 to 29|30 to 34|35 to 39|40 to 44|45 to 49|50 to 54|55 to 59|60 to 64|65 years and over|80 to 84|85 years and over|90 to 94"
age_groups = df.loc[df["Variable"].str.contains(age_groups_pattern), area_cols]
std_per_area = age_groups.std()
most_uniform_area = std_per_area.idxmin()
print(f"⚖️ Наиболее равномерное распределение возрастов: {most_uniform_area}")

plt.figure(figsize=(10,5))
age_groups[most_uniform_area].plot(kind="bar", color="purple")
plt.title(f"Распределение возрастов в {most_uniform_area}")
plt.xlabel("Возрастная группа")
plt.ylabel("Численность")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
