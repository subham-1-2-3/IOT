import sqlite3
 
conn = sqlite3.connect('iot_data.db')
c = conn.cursor()
 
c.execute('''
     CREATE TABLE IF NOT EXISTS sensor_data (
         id INTEGER PRIMARY KEY AUTOINCREMENT,
         temperature REAL,
         humidity REAL,
         motor_status TEXT,
         rain_status TEXT,
         soil_moisture INTEGER,
         water_flow REAL,
         timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
     )
 ''')
 
conn.commit()
conn.close()
print("Database and table created.")