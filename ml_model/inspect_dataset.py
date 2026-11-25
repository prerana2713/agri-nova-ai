import pandas as pd

# Read the Kaggle dataset
data = pd.read_csv("fertilizer_dataset_kaggle.csv")

# Display basic information
print("DATASET LOADED SUCCESSFULLY")

print("\nNumber of rows and columns:")
print(data.shape)

print("\nColumn names:")
print(data.columns.tolist())

print("\nFirst 5 records:")
print(data.head())

print("\nMissing values:")
print(data.isnull().sum())
print("\nDataset size:")
print("Rows:", data.shape[0])
print("Columns:", data.shape[1])
print("\nUnique fertilizer names:")
print(data["Fertilizer Name"].unique())

print("\nFertilizer counts:")
print(data["Fertilizer Name"].value_counts())
print("\nCrop types:")
print(data["Crop Type"].value_counts())

print("\nSoil types:")
print(data["Soil Type"].value_counts())

print("\nData types:")
print(data.dtypes)