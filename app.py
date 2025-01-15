from flask import Flask, request, jsonify, send_from_directory
import joblib
import pandas as pd
import os

app = Flask(__name__)

# Load the pre-trained model
model = joblib.load('energy_model.pkl')

# Define the root route to serve the frontend
@app.route('/')
def home():
    return send_from_directory('../frontend', 'index.html')

# Serve static files (like CSS and JS)
@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('../frontend', path)

# Prediction route
@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    df = pd.DataFrame(data, index=[0])
    
    # Ensure the feature names match those used in training
    expected_features = ['year', 'month', 'day_of_week', 'hour', 'temperature', 'humidity', 'occupancy_level', 'is_holiday', 'temperature_squared']
    df = df.reindex(columns=expected_features)
    
    # Handle missing values if necessary
    df.fillna(0, inplace=True)
    
    # Make prediction
    prediction = model.predict(df)

    # New logic for fans and light bulbs
    num_fans_on = int(data.get('num_fans_on', 0))
    num_bulbs_on = int(data.get('num_bulbs_on', 0))

    # Assuming a fixed number of fans and bulbs
    total_fans_required = 3  # Change this as per your requirement
    total_bulbs_required = 2  # Change this as per your requirement

    # Calculate how many need to be turned off
    fans_to_turn_off = max(0, num_fans_on - total_fans_required)
    bulbs_to_turn_off = max(0, num_bulbs_on - total_bulbs_required)

    # Calculate energy savings (assuming some energy values)
    energy_saved = (fans_to_turn_off * 50) + (bulbs_to_turn_off * 10)  # Adjust energy values as needed

    # Prepare response
    response = {
        'prediction': prediction[0],
        'fans_to_turn_off': fans_to_turn_off,
        'bulbs_to_turn_off': bulbs_to_turn_off,
        'energy_saved': energy_saved,
        'appreciation_message': "Good job! You're using your devices wisely!" if fans_to_turn_off == 0 and bulbs_to_turn_off == 0 else ""
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
