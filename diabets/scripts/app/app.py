from flask import Flask, render_template, request, jsonify
import pickle
import random
import json
import time

app = Flask(__name__, static_url_path='', static_folder='static')

def calculate_response_time(f):
    def decorated_function(*args, **kwargs):
        start_time = time.time()
        response = f(*args, **kwargs)
        end_time = time.time()
        response_time = end_time - start_time
        print(f"Response Time for '{request.path}': {response_time:.6f} seconds")
        return response
    return decorated_function

# Load the pre-trained model
with open('modelbest.pkl', 'rb') as file:
    model = pickle.load(file)

# Load responses from a JSON file
with open('responses.json', 'r') as file:
    all_responses = json.load(file)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
@calculate_response_time
def predict():
    try:
        data = request.json
        pregnancies = float(data['pregnancies'])
        glucose = float(data['glucose'])
        blood_pressure = float(data['bloodPressure'])
        heart_rate = float(data['heartRate'])
        insulin = float(data['insulin'])
        bmi = float(data['bmi'])
        diabetes_pedigree = float(data['diabetesPedigree'])
        age = float(data['age'])

        prediction = model.predict([[pregnancies, glucose, blood_pressure, heart_rate, insulin, bmi, diabetes_pedigree, age]])

        result = 'High' if prediction[0] == 1 else 'Low' if prediction[0] == 0 else 'Invalid Prediction'

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
    app.run(debug=True)
