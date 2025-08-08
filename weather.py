import requests

API_KEY = "56e7ec02b81e3d31015462027c5a9061" 
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    if not API_KEY or API_KEY == "YOUR_API_KEY":
        print("Error: API key is missing or not set correctly. Please add your API key in the code.")
        return
    
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"  # Change to "imperial" for Fahrenheit
    }
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        city_name = data["name"]
        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]
        print(f"Weather in {city_name}: {temp}°C, {description}")
    elif response.status_code == 401:
        print("Error: Unauthorized. Check your API key.")
    elif response.status_code == 404:
        print("Error: City not found. Please check the city name.")
    else:
        print("Error fetching data. Check city name or API key.")

if __name__ == "__main__":
    city = input("Enter city name: ")
    get_weather(city)
