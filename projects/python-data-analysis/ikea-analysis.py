import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# =====================================================
# IKEA Furniture Data Analysis
# Author: Pavlo Huz
# =====================================================


# -------------------------
# 1. Load dataset
# -------------------------

file_name = "ikea.csv"

url = (
    "https://raw.githubusercontent.com/"
    "rfordatascience/tidytuesday/master/data/"
    "2020/2020-11-03/ikea.csv"
)

if os.path.exists(file_name):
    print("File already exists")
else:
    response = requests.get(url, timeout=30)

    if response.status_code == 200:
        with open(file_name, "wb") as file:
            file.write(response.content)

        print("File downloaded successfully")
    else:
        print(f"Failed to download file. Status code: {response.status_code}")


df = pd.read_csv(file_name)


# -------------------------
# 2. Initial data exploration
# -------------------------

print("\nFirst rows:")
print(df.head())

print("\nDataset shape:")
print(df.shape)

print("\nDataset info:")
df.info()

print("\nMissing values:")
print(df.isna().sum())

print("\nDuplicated rows:")
print(df.duplicated().sum())


# -------------------------
# 3. Price distribution
# -------------------------

plt.figure(figsize=(10, 6))

df["price"].hist(bins=30)

plt.title("Price Distribution")
plt.xlabel("Price")
plt.ylabel("Number of Products")
plt.tight_layout()
plt.show()


# -------------------------
# 4. Most and least represented categories
# -------------------------

top_3_categories = df["category"].value_counts().head(3)
bottom_3_categories = df["category"].value_counts().tail(3)

categories_comparison = pd.concat(
    [top_3_categories, bottom_3_categories]
).sort_values()

plt.figure(figsize=(10, 6))

categories_comparison.plot(kind="barh")

plt.title("Most and Least Represented Categories")
plt.xlabel("Number of Products")
plt.ylabel("Category")
plt.tight_layout()
plt.show()


# -------------------------
# 5. Average price by category
# -------------------------

avg_price = (
    df.groupby("category")["price"]
    .mean()
    .sort_values()
)

plt.figure(figsize=(10, 7))

avg_price.plot(kind="barh")

plt.title("Average Price by Category")
plt.xlabel("Average Price")
plt.ylabel("Category")
plt.tight_layout()
plt.show()


# -------------------------
# 6. Median price by category
# -------------------------

median_price = (
    df.groupby("category")["price"]
    .median()
    .sort_values()
)

plt.figure(figsize=(10, 7))

median_price.plot(kind="barh")

plt.title("Median Price by Category")
plt.xlabel("Median Price")
plt.ylabel("Category")
plt.tight_layout()
plt.show()


# -------------------------
# 7. Top 10 designers
# -------------------------

top_10_designers = (
    df["designer"]
    .value_counts()
    .head(10)
    .sort_values()
)

plt.figure(figsize=(10, 6))

top_10_designers.plot(kind="barh")

plt.title("Top 10 Designers by Number of Products")
plt.xlabel("Number of Products")
plt.ylabel("Designer")
plt.tight_layout()
plt.show()


# -------------------------
# 8. Width vs price
# -------------------------

width_price_data = df.loc[
    df["width"].notna(),
    ["width", "price"]
]

plt.figure(figsize=(10, 6))

plt.scatter(
    width_price_data["width"],
    width_price_data["price"],
    alpha=0.6
)

plt.title("Relationship Between Width and Price")
plt.xlabel("Width")
plt.ylabel("Price")
plt.tight_layout()
plt.show()


# -------------------------
# 9. Correlation analysis
# -------------------------

dimensions_price = df[
    ["depth", "height", "width", "price"]
].dropna()

correlation_matrix = dimensions_price.corr()

print("\nCorrelation Matrix:")
print(correlation_matrix)

plt.figure(figsize=(8, 6))

sns.heatmap(
    correlation_matrix,
    annot=True,
    fmt=".2f",
    cmap="Blues",
    square=True
)

plt.title("Correlation Matrix")
plt.tight_layout()
plt.show()


# -------------------------
# 10. Data preprocessing
# -------------------------

features = [
    "category",
    "designer",
    "other_colors",
    "depth",
    "height",
    "width"
]

prepared_data = df[features].copy()


# Convert Yes / No to binary values
prepared_data["other_colors"] = prepared_data["other_colors"].replace({
    "Yes": 1,
    "No": 0
})

prepared_data["other_colors"] = (
    prepared_data["other_colors"]
    .astype(int)
)


# Fill missing numerical values using
# median values within each category
prepared_data["depth"] = prepared_data["depth"].fillna(
    prepared_data.groupby("category")["depth"]
    .transform("median")
)

prepared_data["height"] = prepared_data["height"].fillna(
    prepared_data.groupby("category")["height"]
    .transform("median")
)

prepared_data["width"] = prepared_data["width"].fillna(
    prepared_data.groupby("category")["width"]
    .transform("median")
)


# Encode categorical variables
prepared_data = pd.get_dummies(
    prepared_data,
    columns=["category", "designer"],
    drop_first=True
)


# -------------------------
# 11. Final preprocessing check
# -------------------------

print("\nPrepared Data:")
print(prepared_data.head())

print("\nPrepared Data Shape:")
print(prepared_data.shape)

print("\nRemaining Missing Values:")
print(prepared_data.isna().sum())
