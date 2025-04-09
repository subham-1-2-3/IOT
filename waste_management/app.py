from flask import Flask, render_template_string
import sqlite3
import random
import datetime

app = Flask(__name__)
DB_NAME = "smart_waste.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
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

    cursor.execute("SELECT COUNT(*) FROM waste_data")
    if cursor.fetchone()[0] == 0:
        bin_ids = ['BIN_A1', 'BIN_B2', 'BIN_C3']
        for _ in range(10):
            for bin_id in bin_ids:
                timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                fill_level = random.randint(10, 100)
                gas_level = random.randint(0, 10)
                temperature = round(random.uniform(25, 35), 2)
                humidity = round(random.uniform(40, 70), 2)
                cursor.execute('''
                    INSERT INTO waste_data (timestamp, bin_id, fill_level, gas_level, temperature, humidity)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (timestamp, bin_id, fill_level, gas_level, temperature, humidity))
        conn.commit()
    conn.close()

def fetch_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT bin_id, timestamp, fill_level, gas_level, temperature, humidity
        FROM waste_data
        ORDER BY timestamp DESC
        LIMIT 50
    ''')
    data = cursor.fetchall()
    conn.close()
    return data

def get_average_fill_levels():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT bin_id, AVG(fill_level)
        FROM waste_data
        GROUP BY bin_id
    ''')
    results = cursor.fetchall()
    conn.close()
    labels = [row[0] for row in results]
    values = [round(row[1], 2) for row in results]
    return labels, values

@app.route('/')
def index():
    data = fetch_data()
    labels, values = get_average_fill_levels()
    return render_template_string(TEMPLATE, data=data, labels=labels, values=values)

TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Smart Waste Monitoring</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {
            font-family: Arial, sans-serif;
            padding: 40px;
            background-color: #f5f5f5;
        }
        h1 {
            text-align: center;
            color: #00796b;
        }
        .chart-container {
            width: 70%;
            margin: 30px auto;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            background: #fff;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            margin-top: 30px;
        }
        th, td {
            padding: 12px;
            border: 1px solid #ddd;
            text-align: center;
        }
        th {
            background-color: #004d40;
            color: white;
        }
        .alert {
            background-color: #ffdddd;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <h1>Smart Waste Monitoring Dashboard</h1>

    <div class="chart-container">
        <canvas id="fillChart"></canvas>
    </div>

    <p style="text-align:center;">Red rows indicate bins that are over 80% full.</p>
    <table>
        <thead>
            <tr>
                <th>Bin ID</th>
                <th>Timestamp</th>
                <th>Fill Level (%)</th>
                <th>Gas Level</th>
                <th>Temperature (°C)</th>
                <th>Humidity (%)</th>
            </tr>
        </thead>
        <tbody>
            {% for row in data %}
            <tr class="{{ 'alert' if row[2] > 80 else '' }}">
                <td>{{ row[0] }}</td>
                <td>{{ row[1] }}</td>
                <td>{{ row[2] }}</td>
                <td>{{ row[3] }}</td>
                <td>{{ row[4] }}</td>
                <td>{{ row[5] }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>

    <script>
        const ctx = document.getElementById('fillChart').getContext('2d');
        const fillChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: {{ labels | safe }},
                datasets: [{
                    label: 'Average Fill Level (%)',
                    data: {{ values | safe }},
                    backgroundColor: ['#009688', '#26a69a', '#4db6ac'],
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100
                    }
                }
            }
        });
    </script>
</body>
</html>
'''

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
