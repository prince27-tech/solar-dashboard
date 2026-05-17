from flask import Flask, render_template, request, jsonify
from weather import get_weather
import sqlite3

app = Flask(__name__)


# ---------------- DATABASE ----------------

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


# ---------------- ENERGY LOGIC ----------------

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


# ---------------- HOME ----------------

@app.route('/')
def home():

    return render_template('index.html')


# ---------------- PREDICT ----------------

@app.route('/predict', methods=['POST'])
def predict():

    data = request.json

    city = data.get('city', 'Jaipur')

    panel_capacity = float(
        data.get('panel', 5)
    )

    temp, clouds, radiation, daily = get_weather(city)

    if temp is None:

        temp = 25
        clouds = 50
        radiation = 500

    energy, efficiency = calculate_energy(
        radiation,
        panel_capacity,
        temp
    )

    insert_data(
        city,
        energy,
        efficiency
    )

    # ---------- 7 DAY FORECAST ----------

    forecast = []

    daily_radiation = daily['shortwave_radiation_sum']

    daily_temp = daily['temperature_2m_max']

    for i in range(7):

        future_energy, _ = calculate_energy(
            daily_radiation[i],
            panel_capacity,
            daily_temp[i]
        )

        forecast.append(future_energy)

    return jsonify({

        "temperature": temp,

        "clouds": clouds,

        "radiation": radiation,

        "energy": energy,

        "efficiency": efficiency,

        "forecast": forecast,

        "city": city
    })




if __name__ == '__main__':

    import os

if __name__ == '__main__':

    port = int(os.environ.get("PORT", 5000))

    app.run(host='0.0.0.0', port=port)