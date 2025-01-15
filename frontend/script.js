document.getElementById('prediction-form').addEventListener('submit', function (event) {
    event.preventDefault();
    
    // Collect form data
    const formData = {
        year: document.getElementById('year').value,
        month: document.getElementById('month').value,
        day_of_week: document.getElementById('day_of_week').value,
        hour: document.getElementById('hour').value,
        temperature: document.getElementById('temperature').value,
        humidity: document.getElementById('humidity').value,
        occupancy_level: document.getElementById('occupancy_level').value,
        is_holiday: document.getElementById('is_holiday').value,
        temperature_squared: Math.pow(document.getElementById('temperature').value, 2),
        num_fans_on: document.getElementById('num_fans_on').value, // New input
        num_bulbs_on: document.getElementById('num_bulbs_on').value  // New input
    };

    // Send AJAX request
    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        // Display the prediction result and additional information
        let resultHTML = `Predicted Energy Consumption: ${data.prediction}<br>`;
        resultHTML += `Fans to turn off: ${data.fans_to_turn_off}<br>`;
        resultHTML += `Bulbs to turn off: ${data.bulbs_to_turn_off}<br>`;
        resultHTML += `Energy saved: ${data.energy_saved} units<br>`;
        
        if (data.appreciation_message) {
            resultHTML += `<strong>${data.appreciation_message}</strong>`;
        }
        
        document.getElementById('result').innerHTML = resultHTML;
    })
    .catch(error => console.error('Error:', error));
});
