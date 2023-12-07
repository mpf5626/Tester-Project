from flask import Flask, render_template, request
import requests

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
        weather_data = {
            'city': data['name'],
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed'],
            'icon': data['weather'][0]['icon'],
        }
        return render_template('weather.html', weather_data=weather_data)
    else:
        error_message = 'City not found. Please enter a valid city name.'
        return render_template('error.html', error_message=error_message)

# ...


if __name__ == '__main__':
    app.run(debug=True)
