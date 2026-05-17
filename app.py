from flask import Flask, render_template, request, jsonify
from weather import get_weather

import sqlite3
import os
import random

app = Flask(__name__)


# -------- DATABASE --------

def insert_data(city, energy, efficiency):

    conn = sqlite3.connect('database.db')

    c = conn.cursor()

    c.execute("""

    CREATE TABLE IF NOT EXISTS energy (

        city TEXT,

        energy REAL,

        efficiency REAL

    )

    """)

    c.execute(

        "INSERT INTO energy (city, energy, efficiency) VALUES (?, ?, ?)",

        (city, energy, efficiency)

    )

    conn.commit()

    conn.close()



# -------- ENERGY CALCULATION --------

def calculate_energy(

    radiation,

    panel_capacity,

    temp

):

    energy = (

        radiation / 1000

    ) * panel_capacity


    efficiency = 100 - abs(temp - 25) * 1.2


    if efficiency < 50:

        efficiency = 50


    final_energy = energy * (efficiency / 100)


    return round(final_energy, 2), round(efficiency, 2)



# -------- HOME --------

@app.route('/')

def home():

    return render_template('index.html')



# -------- PREDICT --------

@app.route('/predict', methods=['POST'])

def predict():

    data = request.json

    city = data.get('city', 'Jaipur')

    panel_capacity = float(

        data.get('panel', 5)

    )


    weather_data = get_weather(city)


    if weather_data is None:

        return jsonify({

            "error": "Weather API failed"

        })


    temp = weather_data['temp']

    clouds = weather_data['clouds']

    radiation = weather_data['radiation']


    # -------- CURRENT ENERGY --------

    energy, efficiency = calculate_energy(

        radiation,

        panel_capacity,

        temp

    )


    energy = energy * 100


    insert_data(

        city,

        energy,

        efficiency

    )


    # -------- FORECAST --------

    forecast_energy = []


    for i in range(7):

        future_energy, _ = calculate_energy(

            weather_data['forecast_radiation'][i],

            panel_capacity,

            weather_data['forecast_temp'][i]

        )


        future_energy = (

            future_energy * 100

        ) + random.uniform(-3, 3)


        forecast_energy.append(

            round(future_energy, 2)

        )


    return jsonify({

        "temperature": round(temp, 1),

        "clouds": round(clouds, 1),

        "radiation": round(radiation, 1),

        "energy": round(energy, 2),

        "efficiency": round(efficiency, 2),

        "forecast": forecast_energy,

        "forecast_days": weather_data['days'],

        "forecast_temp": weather_data['forecast_temp'],

        "hourly_temp": weather_data['hourly_temp'],

        "hourly_radiation": weather_data['hourly_radiation'],

        "city": city

    })



# -------- RUN --------

if __name__ == '__main__':

    port = int(os.environ.get("PORT", 5000))

    app.run(

        host='0.0.0.0',

        port=port

    )