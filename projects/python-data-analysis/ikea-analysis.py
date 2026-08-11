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
        print(
            f"Failed to download file. "
            f"Status code: {response.status_code}"
        )


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

print("\nPrice statistics:")
print(df["price"].describe())


# -------------------------
# 3. Data cleaning
# -------------------------

# Remove unnecessary column
df = df.drop(
    columns=["Unnamed: 0"],
    errors="ignore"
)

# Remove duplicated rows
df = df.drop_duplicates()

# Clean designer column
# Some rows contain product codes instead of designer names
bad_designer = df["designer"].str.contains(
    r"\d",
    na=False
)

df.loc[
    bad_designer,
    "designer"
] = "Unknown"


# Clean old_price column
df["old_price"] = (
    df["old_price"]
    .astype(str)
    .str.replace("SR", "", regex=False)
    .str.replace(",", "", regex=False)
    .str.extract(r"(\d+\.?\d*)")[0]
)

df["old_price"] = pd.to_numeric(
    df["old_price"],
    errors="coerce"
)

df["old_price"] = df["old_price"].fillna(
    df["price"]
)


# Fill missing dimensions
# using median values within each category
df["depth"] = df["depth"].fillna(
    df.groupby("category")["depth"]
    .transform("median")
)

df["height"] = df["height"].fillna(
    df.groupby("category")["height"]
    .transform("median")
)

df["width"] = df["width"].fillna(
    df.groupby("category")["width"]
    .transform("median")
)


print("\nMissing values after cleaning:")
print(df.isna().sum())

print("\nDuplicated rows after cleaning:")
print(df.duplicated().sum())


# -------------------------
# 4. Dataset summary
# -------------------------

print("\nDataset Summary:")

print(
    "Number of products:",
    len(df)
)

print(
    "Number of categories:",
    df["category"].nunique()
)

print(
    "Number of designers:",
    df["designer"].nunique()
)

print(
    "Average price:",
    round(df["price"].mean(), 2)
)

print(
    "Median price:",
    round(df["price"].median(), 2)
)


# -------------------------
# 5. Price distribution
# -------------------------

plt.figure(figsize=(10, 6))

df["price"].hist(
    bins=30,
    edgecolor="black"
)

plt.title("Price Distribution")
plt.xlabel("Price")
plt.ylabel("Number of Products")

plt.tight_layout()
plt.show()


# -------------------------
# 6. Most and least represented categories
# -------------------------

top_3_categories = (
    df["category"]
    .value_counts()
    .head(3)
)

bottom_3_categories = (
    df["category"]
    .value_counts()
    .tail(3)
)

categories_comparison = pd.concat(
    [
        top_3_categories,
        bottom_3_categories
    ]
).sort_values()

plt.figure(figsize=(10, 6))

categories_comparison.plot(
    kind="barh"
)

plt.title(
    "Most and Least Represented Categories"
)

plt.xlabel("Number of Products")
plt.ylabel("Category")

plt.tight_layout()
plt.show()


# -------------------------
# 7. Average price by category
# -------------------------

avg_price = (
    df.groupby("category")["price"]
    .mean()
    .sort_values()
)

plt.figure(figsize=(10, 7))

avg_price.plot(
    kind="barh"
)

plt.title(
    "Average Price by Category"
)

plt.xlabel("Average Price")
plt.ylabel("Category")

plt.tight_layout()
plt.show()


# -------------------------
# 8. Median price by category
# -------------------------

median_price = (
    df.groupby("category")["price"]
    .median()
    .sort_values()
)

plt.figure(figsize=(10, 7))

median_price.plot(
    kind="barh"
)

plt.title(
    "Median Price by Category"
)

plt.xlabel("Median Price")
plt.ylabel("Category")

plt.tight_layout()
plt.show()


# -------------------------
# 9. Category summary
# -------------------------

category_summary = (
    df.groupby("category")
    .agg(
        products=("item_id", "count"),
        average_price=("price", "mean"),
        median_price=("price", "median")
    )
    .sort_values(
        "products",
        ascending=False
    )
)

print("\nCategory Summary:")
print(category_summary)


# -------------------------
# 10. Top 10 designers
# -------------------------

top_10_designers = (
    df["designer"]
    .value_counts()
    .head(10)
    .sort_values()
)

plt.figure(figsize=(10, 6))

top_10_designers.plot(
    kind="barh"
)

plt.title(
    "Top 10 Designers by Number of Products"
)

plt.xlabel("Number of Products")
plt.ylabel("Designer")

plt.tight_layout()
plt.show()


# -------------------------
# 11. Top 10 most expensive products
# -------------------------

top_expensive = (
    df[
        [
            "name",
            "category",
            "designer",
            "price"
        ]
    ]
    .sort_values(
        "price",
        ascending=False
    )
    .head(10)
)

print("\nTop 10 Most Expensive Products:")
print(top_expensive)


# -------------------------
# 12. Width vs price
# -------------------------

plt.figure(figsize=(10, 6))

plt.scatter(
    df["width"],
    df["price"],
    alpha=0.5
)

plt.title(
    "Relationship Between Width and Price"
)

plt.xlabel("Width")
plt.ylabel("Price")

plt.tight_layout()
plt.show()


# -------------------------
# 13. Correlation analysis
# -------------------------

dimensions_price = df[
    [
        "depth",
        "height",
        "width",
        "price"
    ]
]

correlation_matrix = (
    dimensions_price.corr()
)

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
