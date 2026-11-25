
import pandas as pd

# Load the dataset
data = pd.read_csv("fertilizer_dataset_kaggle.csv")

# Remove extra spaces from column names
data.columns = data.columns.str.strip()

# Display dataset information
print("Original dataset shape:", data.shape)

# Check duplicate records
print("\nDuplicate records:", data.duplicated().sum())

# Remove duplicate records
data = data.drop_duplicates()

# Check missing values
print("\nMissing values:")
print(data.isnull().sum())

# Display crop and soil categories
print("\nCrop categories:")
print(data["Crop Type"].value_counts())

print("\nSoil categories:")
print(data["Soil Type"].value_counts())

# Save the cleaned dataset
data.to_csv("cleaned_fertilizer_dataset.csv", index=False)

print("\nCleaned dataset saved successfully!")
print("Final dataset shape:", data.shape)
