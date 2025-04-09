from flask import Flask, render_template
import sqlite3
import random
 
app = Flask(__name__)
 
def insert_random_data():
     conn = sqlite3.connect('iot_data.db')
     c = conn.cursor()
     
     # Generate random values
     temperature = round(random.uniform(20.0, 40.0), 2)
     humidity = round(random.uniform(30.0, 90.0), 2)
     motor_status = random.choice(["ON", "OFF"])
     rain_status = random.choice(["Detected", "Not Detected"])
     soil_moisture = random.randint(200, 800)
     water_flow = round(random.uniform(1.0, 10.0), 2)
 
     # Insert into database
     c.execute('''
         INSERT INTO sensor_data (temperature, humidity, motor_status, rain_status, soil_moisture, water_flow)
         VALUES (?, ?, ?, ?, ?, ?)
     ''', (temperature, humidity, motor_status, rain_status, soil_moisture, water_flow))
 
     conn.commit()
     conn.close()
 
def get_latest_data():
     conn = sqlite3.connect('iot_data.db')
     c = conn.cursor()
     c.execute('SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT 1')
     row = c.fetchone()
     conn.close()
     if row:
         return {
             'temperature': row[1],
             'humidity': row[2],
             'motor_status': row[3],
             'rain_status': row[4],
             'soil_moisture': row[5],
             'water_flow': row[6]
         }
     return None
 
@app.route('/')
def index():
     insert_random_data()  # 👈 generate new data every time
     data = get_latest_data()
     return render_template("index.html", **data)
 
if __name__ == '__main__':
     app.run(debug=True)