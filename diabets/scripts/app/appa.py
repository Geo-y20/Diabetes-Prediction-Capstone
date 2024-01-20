from flask import Flask, render_template, request, jsonify
import pickle
import traceback
from werkzeug.exceptions import UnsupportedMediaType
import serial
import random
import json
import time

app = Flask(__name__)
serialcom = serial.Serial('COM8', 9600)
serialcom.timeout = 1

#model = pickle.load(open('modelgc.pkl', 'rb'))
with open('modelbest.pkl', 'rb') as file:
    model = pickle.load(file)

# Load responses from a JSON file
with open('responses.json', 'r') as file:
    all_responses = json.load(file)

@app.route('/')
def index():
    heart_rate = get_sensor_data()
    return render_template('indexa.html', heart_rate=heart_rate)

def calculate_response_time(f):
    def decorated_function(*args, **kwargs):
        start_time = time.time()
        response = f(*args, **kwargs)
        end_time = time.time()
        response_time = end_time - start_time
        print(f"Response Time for '{request.path}': {response_time:.6f} seconds")
        return response
    return decorated_function

def send_command(command):
    serialcom.write(command.encode())  # Send command to Arduino

def get_sensor_data():
    try:
        data = serialcom.readline().decode().strip()
        return data
    except serial.SerialException as e:
        print("Serial communication error:", e)
        return "Sensor data not available"

@app.route('/predict', methods=['POST'])
@calculate_response_time
def predict():
    try:
        data = request.json
        pregnancies = float(data['pregnancies'])
        glucose = float(data['glucose'])
        blood_pressure = float(data['bloodPressure'])
        heart_rate = get_sensor_data()  # Get sensor data
        Heart_r = float(heart_rate)
        insulin = float(data['insulin'])
        bmi = float(data['bmi'])
        diabetes_pedigree = float(data['diabetesPedigree'])
        age = float(data['age'])

        prediction = model.predict([[pregnancies, glucose, blood_pressure, Heart_r, insulin, bmi, diabetes_pedigree, age]])

        result = 'Having Diabetes' if prediction[0] == 1 else 'Not Having Diabetes' if prediction[0] == 0 else 'Invalid Prediction'

        send_command(result)
        return jsonify({'prediction': result})

    except Exception as e:
        return jsonify({'error': 'Invalid input or model error'}), 400

@app.route('/check_diabetes', methods=['GET', 'POST'])
def check_diabetes():
    if request.method == 'POST':
        user_input = request.form.get('user_input')
        if user_input == 'I am diabetes patient':
            response_data = random.choice(all_responses['diabetes_responses'])
        else:
            response_data = random.choice(all_responses['non_diabetes_responses'])
    else:
        response_data = {"response": "", "advice": ""}

    return render_template('check_diabetes.html', response=response_data["response"], advice=response_data["advice"])





if __name__ == '__main__':
    app.run()
