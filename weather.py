import requests


def get_weather(city="Jaipur"):

    try:

        # -------- CITY COORDINATES --------

        geo_url = (

            f"https://geocoding-api.open-meteo.com/v1/search?"
            f"name={city}&count=1"

        )

        geo_response = requests.get(geo_url).json()

        latitude = geo_response['results'][0]['latitude']

        longitude = geo_response['results'][0]['longitude']


        # -------- WEATHER + FORECAST --------

        weather_url = (

            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={latitude}"
            f"&longitude={longitude}"
            f"&current=temperature_2m,cloud_cover,shortwave_radiation"
            f"&hourly=temperature_2m,shortwave_radiation"
            f"&daily=temperature_2m_max,shortwave_radiation_sum"
            f"&forecast_days=7"

        )

        weather_response = requests.get(weather_url).json()

        current = weather_response['current']

        hourly = weather_response['hourly']

        daily = weather_response['daily']


        # -------- CURRENT DATA --------

        temp = current['temperature_2m']

        clouds = current['cloud_cover']

        radiation = current['shortwave_radiation']


        # -------- FORECAST --------

        forecast_days = daily['time']

        forecast_temp = daily['temperature_2m_max']

        forecast_radiation = daily['shortwave_radiation_sum']


        return {

            "temp": temp,

            "clouds": clouds,

            "radiation": radiation,

            "days": forecast_days,

            "forecast_temp": forecast_temp,

            "forecast_radiation": forecast_radiation,

            "hourly_temp": hourly['temperature_2m'][:24],

            "hourly_radiation": hourly['shortwave_radiation'][:24]

        }


    except Exception as e:

        print("Weather Error:", e)

        return None