import sqlite3
import random
import time
from datetime import datetime

conn = sqlite3.connect('smart_waste.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS waste_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    bin_id TEXT,
    fill_level INTEGER,
    gas_level INTEGER,
    temperature REAL,
    humidity REAL
)
''')
conn.commit()

def simulate_sensor_data(bin_id):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    fill_level = random.randint(10, 100)        
    gas_level = random.randint(0, 10)           
    temperature = round(random.uniform(25, 35), 2)
    humidity = round(random.uniform(40, 70), 2)

    cursor.execute('''
    INSERT INTO waste_data (timestamp, bin_id, fill_level, gas_level, temperature, humidity)
    VALUES (?, ?, ?, ?, ?, ?)''',
    (timestamp, bin_id, fill_level, gas_level, temperature, humidity))

    conn.commit()
    print(f"Inserted: Bin {bin_id} at {timestamp} | Fill: {fill_level}% | Gas: {gas_level} | Temp: {temperature}°C")

bin_ids = ['BIN_A1', 'BIN_B2', 'BIN_C3']
for i in range(10):
    for bin_id in bin_ids:
        simulate_sensor_data(bin_id)
    time.sleep(1)  

conn.close()
