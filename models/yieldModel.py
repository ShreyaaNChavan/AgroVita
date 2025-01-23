import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib

# Step 1: Load the Dataset from a CSV File
file_path = r"C:\Users\admin\ShreyaProjects\IBM\data\crop_yield_data.csv"  # Replace with the actual path to your file
df = pd.read_csv(file_path)

# Step 2: Define Features (X) and Target (y)
X = df[["rainfall_mm", "soil_quality_index", "farm_size_hectares", "sunlight_hours", "fertilizer_kg"]]
y = df["crop_yield"]

# Step 3: Split the Data into Training and Testing Sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 4: Train a Machine Learning Model
model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)

# Step 5: Evaluate the Model
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("Model Evaluation:")
print(f"Mean Squared Error (MSE): {mse}")
print(f"R-squared (R2): {r2}")

# Step 6: Save the Trained Model Locally
model_filename = "crop_yield_model.pkl"
joblib.dump(model, model_filename)

print(f"Model saved as {model_filename}")
