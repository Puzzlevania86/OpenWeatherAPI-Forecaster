import requests as rq
import os
from dotenv import load_dotenv

BASE_URL = "https://api.openweathermap.org/geo/1.0/direct"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

if __name__ == "__main__":
    load_dotenv()
    
    APIKEY = os.environ.get("APIKEY")
    
    city = input("Print the name of the city: ")
    code = input("Print the state code if applicable: ")
    country = input("Print the name of the country: ")
    
    parameters = {
        "q": f"{city}, {code}, {country}",
        "appid": APIKEY
    }  
    
    try:
        res = rq.get(BASE_URL, params=parameters)
        res.raise_for_status()
        data = res.json()
        
        if not data:
            print("No data found under those names.")
            quit()
        
        lat = data[0].get("lat")
        lon = data[0].get("lon")
        
        print(f"Latitude: {lat} and Longitude: {lon}")
        
        forecast_params = {
            "lat": lat,
            "lon": lon,
            "appid": APIKEY,
            "units": "imperial"
        }
        
        forecast = rq.get(FORECAST_URL, params=forecast_params)
        forecast.raise_for_status()
        forecast_data = forecast.json()
        
        weather = []
        for data in forecast_data["list"]:
            if data["dt_txt"].endswith("12:00:00"):
                weather.append(data)
        
        for entry in weather:
            date = entry["dt_txt"].split("-")[1] + "/" + entry["dt_txt"].split("-")[2].replace("12:00:00", "").strip()
            temp = entry["main"].get("temp")
            feels_like = entry["main"].get("feels_like")
            des = entry["weather"][0].get("description")
            print(f"""            On {date}, {city} will experience {des}
            At 12:00, there will be a temperature around {temp}°F, but it will feel like {feels_like}.\n""")
        
    except rq.exceptions.RequestException as e:
        print(f"Your program ran into an exception: {e}")
        
    