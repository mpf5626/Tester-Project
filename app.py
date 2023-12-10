from flask import Flask, render_template, request
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# ...

@app.route('/weather', methods=['POST'])
def weather():
    city = request.form['city']
    api_key = 'e708f9298fb72d34d100684f34dd369e'  # Replace this with your actual API key
    api_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    
    response = requests.get(api_url)
    data = response.json()

    if 'name' in data:

        # Extract timezone information from OpenWeatherMap API
        timezone_offset = data['timezone']

        # Calculate current time using timezone information
        current_utc_time = datetime.utcnow()
        current_local_time = current_utc_time + timedelta(seconds=timezone_offset)

        # Extract Celsius temperature
        temperature_celsius = round(data['main']['temp'], 1)

        # Extract Fahrenheit temperature
        temperature_fahrenheit = round(temperature_celsius * 9/5 + 32, 1)
        
        # Extract precipitation percentage
        precipitation_percent = data.get('rain', {}).get('1h', 0)

        weather_data = {
            'city': data['name'],
            'temperature_celsius': temperature_celsius,
            'temperature_fahrenheit': temperature_fahrenheit,
            'description': data['weather'][0]['description'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed'],
            'icon': data['weather'][0]['icon'],
            'timezone': data['timezone'],
            'current_time': current_local_time.strftime('%Y-%m-%d %H:%M:%S'),
            'precipitation_percent': precipitation_percent,
        }
        
        return render_template('weather.html', weather_data=weather_data)
    else:
        error_message = 'City not found. Please enter a valid city name.'
        return render_template('error.html', error_message=error_message)

# ...


if __name__ == '__main__':
    app.run(debug=True)
