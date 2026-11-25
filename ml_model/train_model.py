
import pandas as pd

# Load the cleaned dataset
data = pd.read_csv("cleaned_fertilizer_dataset.csv")
# Clean column names and text values
data.columns = data.columns.str.strip()
data.rename(columns={"Temparature": "Temperature"}, inplace=True)

data["Soil Type"] = data["Soil Type"].str.strip()
data["Crop Type"] = data["Crop Type"].str.strip()
data["Fertilizer Name"] = data["Fertilizer Name"].str.strip()

# Display dataset information
print("Dataset loaded successfully!")
print("Dataset shape:", data.shape)

print("\nAvailable columns:")
print(data.columns.tolist())

print("\nFirst 5 records:")
print(data.head())

# Separate input features and output target

X = data.drop("Fertilizer Name", axis=1)
y = data["Fertilizer Name"]

print("\nInput features:")
print(X.head())

print("\nOutput target:")
print(y.head())

print("\nInput shape:", X.shape)
print("Output shape:", y.shape)

# Convert text categories into numerical values

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

# Identify text columns
categorical_columns = ["Soil Type", "Crop Type"]

# Convert categories into numbers
preprocessor = ColumnTransformer(
    transformers=[
        ("category", OneHotEncoder(handle_unknown="ignore"), categorical_columns)
    ],
    remainder="passthrough"
)

# Transform input data
X_encoded = preprocessor.fit_transform(X)

print("\nData converted successfully!")
print("Original input shape:", X.shape)
print("Encoded input shape:", X_encoded.shape)

# Split dataset into training and testing data

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("\nDataset split successfully!")

print("Training input:", X_train.shape)
print("Testing input:", X_test.shape)

print("Training output:", y_train.shape)
print("Testing output:", y_test.shape)

# Train the Random Forest model

from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score

# Create the complete machine learning pipeline
model = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", RandomForestClassifier(
        n_estimators=100,
        random_state=42
    ))
])

# Train the model
model.fit(X_train, y_train)

print("\nModel training completed successfully!")

# Test the model
y_pred = model.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)

print("Model accuracy:", round(accuracy * 100, 2), "%")

# Save the trained machine learning model

import joblib

joblib.dump(model, "fertilizer_model.pkl")

print("\nModel saved successfully!")
print("Saved as: fertilizer_model.pkl")
