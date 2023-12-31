import pandas as pd
import numpy as np

# Load the CSV file into a DataFrame
df = pd.read_csv('G:\Data Science Track\Diabetes Prediction\diabets\data\diabetes.csv')  # Replace 'your_dataset.csv' with your file path

# Simulate heart rate readings based on glucose levels
def generate_pulse_sensor_readings(glucose):
    if glucose >= 100:
        return np.random.randint(20, 31) + np.random.randint(20, 31)  # Large increase
    elif glucose >= 50:
        return np.random.randint(10, 16) + np.random.randint(20, 31)  # Moderate increase
    else:
        return np.random.randint(5, 11) + np.random.randint(20, 31)   # Small increase

# Apply function to create a new 'HeartRate' column based on 'Glucose' levels
df['HeartRate'] = df['Glucose'].apply(generate_pulse_sensor_readings)

# Save the modified DataFrame with heart rate readings to a new CSV file
df.to_csv('modified_dataset.csv', index=False)  # Replace 'your_modified_dataset.csv' with desired file path
