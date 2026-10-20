import requests
from datetime import datetime
from zoneinfo import ZoneInfo
url = "https://geocoding-api.open-meteo.com/v1/search"

def get_coordinates(url, params):
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        results = data.get("results")
        if not results:
            print("City does not exist.")
            return
        location = results[0]
        latitude = location["latitude"]
        longitude = location["longitude"]
    except requests.exceptions.HTTPError:
        print("An HTTP error occurred.")
    except requests.exceptions.ConnectionError:
        print("Connection error occurred while obtaining data.")
    except requests.exceptions.Timeout:
        print("The request timed out.")
    except (requests.exceptions.RequestException, ValueError, KeyError, TypeError):
        print("An error occurred while retrieving city coordinates.")
    else:
        return latitude, longitude

def get_weather_condition(weather_code):
    if weather_code == 0:
        return "clear"
    elif weather_code in (1, 2, 3):
        return "cloudy"
    elif weather_code in (45, 48):
        return "fog"
    elif 51 <= weather_code <= 67 or 80 <= weather_code <= 82:
        return "rain"
    elif 71 <= weather_code <= 77:
        return "snow"
    elif weather_code in (95, 96, 99):
        return "storm"
    return "unknown"

def get_weather(latitude, longitude):
    weather_params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": ("temperature_2m,relative_humidity_2m,""wind_speed_10m,weather_code"),
        "temperature_unit": "celsius",
        "wind_speed_unit": "kmh"
    }
    url2 = "https://api.open-meteo.com/v1/forecast"
    try:
        response = requests.get(url2,params=weather_params,timeout=10)
        response.raise_for_status()
        return True, response.json()
    except requests.exceptions.HTTPError:
        return False, "An HTTP error occurred."
    except requests.exceptions.ConnectionError:
        return False, "Connection error occurred while obtaining data."
    except requests.exceptions.Timeout:
        return False, "The weather request timed out."
    except requests.exceptions.JSONDecodeError:
        return False, "Data was not available in the correct format."
    except requests.exceptions.RequestException:
        return False, "An unknown error occurred."

def get_data(latitude, longitude, name):
    weather_data = get_weather(latitude, longitude)
    if not weather_data[0]:
        return weather_data
    response_data = weather_data[1]
    current = response_data.get("current")
    timezone = response_data.get("timezone")
    current_units = response_data.get("current_units")
    if current is None or current_units is None:
        return False, "Necessary weather data is not accessible."
    if not timezone:
        return False, f"Unable to retrieve the time zone of {name}."
    parameters = ["temperature_2m","relative_humidity_2m","wind_speed_10m","weather_code"]
    for parameter in parameters:
        if parameter not in current or parameter not in current_units:
            return False, f"Weather data for {name} is incomplete."
    try:
        city_timezone = ZoneInfo(timezone)
        time_diff = delay_info(current, city_timezone)
    except (ValueError, TypeError, KeyError):
        return False, f"Unable to process the weather timestamp for {name}."
    except Exception as error:
        if isinstance(error, (KeyboardInterrupt, SystemExit)):
            raise
        return False, f"Unable to process the time zone for {name}."
    weather_code = current["weather_code"]
    data = {
        "temperature": current["temperature_2m"],
        "humidity": current["relative_humidity_2m"],
        "wind": current["wind_speed_10m"],
        "temperature_units": current_units["temperature_2m"],
        "humidity_units": current_units["relative_humidity_2m"],
        "wind_units": current_units["wind_speed_10m"],
        "condition": get_weather_condition(weather_code),
    }
    return True, (data, time_diff)

def delay_info(current, city_timezone):
    current_time = datetime.now(city_timezone)
    retrieve_time = datetime.fromisoformat(current["time"])
    if retrieve_time.tzinfo is None:
        retrieve_time = retrieve_time.replace(tzinfo=city_timezone)
    else:
        retrieve_time = retrieve_time.astimezone(city_timezone)
    difference = current_time - retrieve_time
    return max(0, difference.total_seconds())

def main():
    print("------------------Weather App-------------------")
    name = input("Enter the name of the city: ").strip()
    if not name:
        print("Please enter a city name.")
        return
    params = {"name": name}
    result = get_coordinates(url, params)
    if result is None:
        return
    latitude, longitude = result
    details = get_data(latitude, longitude, name)
    if not details[0]:
        print(details[1])
        return
    place_info, time_diff = details[1]
    print(f"Weather in {name}")
    print(f"Temperature: {place_info['temperature']}{place_info['temperature_units']}")
    print(f"Relative Humidity: {place_info['humidity']}{place_info['humidity_units']}")
    print(f"Wind Speed: {place_info['wind']}{place_info['wind_units']}")
    print(f"Condition: {place_info['condition']}")
    minutes = int(time_diff // 60)
    if minutes == 0:
        print(f"Updated {int(time_diff)} seconds ago.")
    else:
        print(f"Updated {minutes} minutes ago.")

if __name__ == "__main__":
    main()