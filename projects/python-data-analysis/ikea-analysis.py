import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# -------------------------
# 1. Load dataset
# -------------------------

file_name = "ikea.csv"
url = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-11-03/ikea.csv"

if os.path.exists(file_name):
    print("File already exists")
else:
    response = requests.get(url)

    if response.status_code == 200:
        with open(file_name, "wb") as file:
            file.write(response.content)
        print("File downloaded")
    else:
        print("Failed to download file")


df = pd.read_csv(file_name)

print(df.head())
print(df.shape)
print(df.info())

print("\nMissing values:")
print(df.isna().sum())

print("\nDuplicates:")
print(df.duplicated().sum())


# -------------------------
# 2. Price distribution
# -------------------------

plt.figure(figsize=(10, 6))
df["price"].hist(bins=30)

plt.title("Price Distribution")
plt.xlabel("Price")
plt.ylabel("Count")
plt.tight_layout()
plt.show()


# -------------------------
# 3. Category analysis
# -------------------------

top_3_categories = df["category"].value_counts().head(3)
bottom_3_categories = df["category"].value_counts().tail(3)

categories_comparison = pd.concat(
    [top_3_categories, bottom_3_categories]
).sort_values()

categories_comparison.plot(kind="barh")

plt.title("Most and Least Represented Categories")
plt.xlabel("Number of Products")
plt.ylabel("Category")
plt.tight_layout()
plt.show()


# -------------------------
# 4. Average price by category
# -------------------------

avg_price = (
    df.groupby("category")["price"]
    .mean()
    .sort_values()
)

avg_price.plot(kind="barh")

plt.title("Average Price by Category")
plt.xlabel("Average Price")
plt.ylabel("Category")
plt.tight_layout()
plt.show()


# -------------------------
# 5. Median price by category
# -------------------------

median_price = (
    df.groupby("category")["price"]
    .median()
    .sort_values()
)

median_price.plot(kind="barh")

plt.title("Median Price by Category")
plt.xlabel("Median Price")
plt.ylabel("Category")
plt.tight_layout()
plt.show()


# -------------------------
# 6. Top 10 designers
# -------------------------

top_10_designers = df["designer"].value_counts().head(10)

top_10_designers.sort_values().plot(kind="barh")

plt.title("Top 10 Designers by Number of Products")
plt.xlabel("Number of Products")
plt.ylabel("Designer")
plt.tight_layout()
plt.show()


# -------------------------
# 7. Width vs price
# -------------------------

width_price_data = df.loc[
    df["width"].notna(),
    ["width", "price"]
]

width_price_data.plot(
    kind="scatter",
    x="width",
    y="price",
    title="Relationship Between Width and Price"
)

plt.xlabel("Width")
plt.ylabel("Price")
plt.tight_layout()
plt.show()


# -------------------------
# 8. Correlation analysis
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
    cmap="Blues"
)

plt.title("Correlation Matrix")
plt.tight_layout()
plt.show()


# -------------------------
# 9. Data preprocessing
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

prepared_data["other_colors"] = prepared_data["other_colors"].replace({
    "Yes": 1,
    "No": 0
})

prepared_data["other_colors"] = prepared_data["other_colors"].astype(int)

prepared_data["depth"] = prepared_data["depth"].fillna(
    prepared_data.groupby("category")["depth"].transform("median")
)

prepared_data["height"] = prepared_data["height"].fillna(
    prepared_data.groupby("category")["height"].transform("median")
)

prepared_data["width"] = prepared_data["width"].fillna(
    prepared_data.groupby("category")["width"].transform("median")
)

prepared_data = pd.get_dummies(
    prepared_data,
    columns=["category", "designer"],
    drop_first=True
)

print("\nPrepared Data:")
print(prepared_data.head())

print("\nPrepared Data Shape:")
print(prepared_data.shape)

print("\nRemaining Missing Values:")
print(prepared_data.isna().sum())
