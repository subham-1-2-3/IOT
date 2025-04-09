import sqlite3
import random
 
def insert_random_data():
     conn = sqlite3.connect('iot_data.db')
     c = conn.cursor()
 
     temperature = round(random.uniform(20, 35), 2)
     humidity = random.randint(40, 90)
     motor_status = random.choice(['ON', 'OFF'])
     rain_status = random.choice(['Rain Detected', 'No Rain'])
     soil_moisture = soil_moisture = random.randint(300, 800)  
 
     water_flow = round(random.uniform(0.5, 3.0), 2)
 
     c.execute('''
     INSERT INTO sensor_data (temperature, humidity, motor_status, rain_status, soil_moisture, water_flow)
     VALUES (?, ?, ?, ?, ?, ?)
 ''', (temperature, humidity, motor_status, rain_status, soil_moisture, water_flow))
 
     conn.commit()
     conn.close()
     print("Inserted one random data record.")
 
insert_random_data()