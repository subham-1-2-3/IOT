import sqlite3
 
def create_database():
     conn = sqlite3.connect('traffic.db')
     c = conn.cursor()
     
     c.execute('''
         CREATE TABLE IF NOT EXISTS traffic_data (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             location TEXT NOT NULL,
             vehicle_count INTEGER NOT NULL,
             avg_speed REAL NOT NULL,
             congestion_level TEXT NOT NULL,
             signal_status TEXT NOT NULL,
             timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
         )
     ''')
     
     conn.commit()
     conn.close()
     print("✅ Database and table created successfully.")
 
if __name__ == '__main__':
     create_database()