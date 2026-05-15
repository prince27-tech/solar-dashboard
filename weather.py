import requests


def get_weather(city="Jaipur"):

    try:

       

        geo_url = (
            f"https://geocoding-api.open-meteo.com/v1/search?"
            f"name={city}&count=1"
        )

        geo_response = requests.get(geo_url).json()

        latitude = geo_response['results'][0]['latitude']
        longitude = geo_response['results'][0]['longitude']


      

        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={latitude}"
            f"&longitude={longitude}"
            f"&current=temperature_2m,cloud_cover,shortwave_radiation"
            f"&daily=temperature_2m_max,shortwave_radiation_sum"
            f"&forecast_days=7"
        )

        weather_response = requests.get(weather_url).json()

        current = weather_response['current']

        daily = weather_response['daily']


       

        temp = current['temperature_2m']

        clouds = current['cloud_cover']

        radiation = current['shortwave_radiation']


        return temp, clouds, radiation, daily


    except Exception as e:

        print("Weather Error:", e)

        return None, None, None, None