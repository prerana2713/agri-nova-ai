
import joblib
import pandas as pd

# Load the saved model
model = joblib.load("fertilizer_model.pkl")

# Enter new soil details
sample = pd.DataFrame([{
    "Temperature": 28,
    "Humidity": 60,
    "Moisture": 40,
    "Soil Type": "Sandy",
    "Crop Type": "Maize",
    "Nitrogen": 30,
    "Potassium": 10,
    "Phosphorous": 15
}])

# Predict fertilizer
prediction = model.predict(sample)

print("Agri Nova AI Prediction")
print("-----------------------")
print("Recommended fertilizer:", prediction[0])
