import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

try:
    # Load dataset
    data = pd.read_csv('C:/Users/Aryan/Desktop/ML miniproject/data/synthetic_energy_data.csv')
    print("Dataset loaded successfully")

    # Convert timestamp to datetime with day first
    data['timestamp'] = pd.to_datetime(data['timestamp'], dayfirst=True)
    data['year'] = data['timestamp'].dt.year
    print("Timestamp column parsed successfully")

    # Define features and target
    X = data[['year', 'month', 'day_of_week', 'hour', 'temperature', 'humidity', 'occupancy_level', 'is_holiday', 'temperature_squared']]
    y = data['energy_consumption']
    print("Features and target defined")

    # Train model
    model = RandomForestRegressor()
    model.fit(X, y)
    print("Model trained successfully")

    # Save model
    joblib.dump(model, 'energy_model.pkl')
    print("Model saved as energy_model.pkl")

except Exception as e:
    print(f"An error occurred: {e}")
