function openCheckDiabetesPage() {
    window.location.href = "/check_diabetes";
}
    
async function predict() {
    const pregnancies = document.getElementById('pregnancies').value;
    const glucose = document.getElementById('glucose').value;
    const bloodPressure = document.getElementById('bloodPressure').value;
    const insulin = document.getElementById('insulin').value;
    const heartRate = document.getElementById('heartRate').value;
    const bmi = document.getElementById('bmi').value;
    const diabetesPedigree = document.getElementById('diabetesPedigree').value;
    const age = document.getElementById('age').value;

    if (!pregnancies || !glucose || !bloodPressure || !insulin || !heartRate || !bmi || !diabetesPedigree || !age) {
        alert('Please fill in all fields!');
        return;
    }

    const formData = {
        pregnancies: parseFloat(pregnancies),
        glucose: parseFloat(glucose),
        bloodPressure: parseFloat(bloodPressure),
        insulin: parseFloat(insulin),
        heartRate: parseFloat(heartRate),
        bmi: parseFloat(bmi),
        diabetesPedigree: parseFloat(diabetesPedigree),
        age: parseFloat(age)
    };

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();
        console.log('Predicted outcome:', data.prediction);
        // You can handle the prediction here (e.g., update the UI)
        // Update the UI to display the prediction result
        const predictionResult = document.getElementById('predictionResult');
        predictionResult.innerHTML = `Predicted outcome: ${data.prediction}`;
    } catch (error) {
        console.error('Error:', error);
    }
}
