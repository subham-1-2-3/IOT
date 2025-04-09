from flask import Flask, render_template, request, redirect
import sqlite3
import random
from datetime import datetime
 
app = Flask(__name__)
 
 # DB setup
def init_db():
     conn = sqlite3.connect('traffic.db')
     c = conn.cursor()
     c.execute('''
         CREATE TABLE IF NOT EXISTS traffic_data (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             location TEXT,
             vehicle_count INTEGER,
             avg_speed REAL,
             congestion_level TEXT,
             signal_status TEXT,
             timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
         )
     ''')
     conn.commit()
     conn.close()
 
 # Simulate sensor data
def insert_fake_data():
     conn = sqlite3.connect('traffic.db')
     c = conn.cursor()
     locations = ["Rasulgarh", "Vani Vihar", "CRP Square", "Jaydev Vihar"]
     for loc in locations:
         count = random.randint(50, 200)
         speed = round(random.uniform(10, 40), 2)
         congestion = "High" if count > 150 else "Moderate" if count > 100 else "Low"
         status = random.choice(["Green", "Red", "Yellow"])
         c.execute('''
             INSERT INTO traffic_data (location, vehicle_count, avg_speed, congestion_level, signal_status)
             VALUES (?, ?, ?, ?, ?)
         ''', (loc, count, speed, congestion, status))
     conn.commit()
     conn.close()
 
@app.route('/')
def index():
     insert_fake_data()  
     conn = sqlite3.connect('traffic.db')
     c = conn.cursor()
     c.execute('''
         SELECT * FROM traffic_data
         ORDER BY timestamp DESC
         LIMIT 4
     ''')
     data = c.fetchall()
     conn.close()
     return render_template('index.html', traffic_data=data)
 
@app.route('/update_signal', methods=['POST'])
def update_signal():
     location = request.form['location']
     new_status = request.form['signal']
     conn = sqlite3.connect('traffic.db')
     c = conn.cursor()
     c.execute('''
         UPDATE traffic_data
         SET signal_status = ?
         WHERE location = ? AND timestamp = (SELECT MAX(timestamp) FROM traffic_data WHERE location = ?)
     ''', (new_status, location, location))
     conn.commit()
     conn.close()
     return redirect('/')
 
if __name__ == '__main__':
     init_db()
     app.run(debug=True)