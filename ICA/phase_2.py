# Author: <Your name here>
# Student ID: <Your Student ID>

import sqlite3
import matplotlib.pyplot as plt

# Database configuration
DB_FILE = "CIS4044-N-SDI-OPENMETEO-PARTIAL.db"

def get_db_connection():
    """Helper function to connect to the database."""
    try:
        conn = sqlite3.connect(DB_FILE)
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def get_city_name(cursor, city_id):
    """
    Helper function to get the name of a city from its ID.
    Returns the name (e.g., 'London') or the ID if not found.
    """
    try:
        cursor.execute("SELECT name FROM cities WHERE id = ?", (city_id,))
        result = cursor.fetchone()
        if result:
            return result[0] # Return the name string
        else:
            return f"Unknown City ({city_id})"
    except Exception:
        return str(city_id)

'''
1. Bar Chart: Precipitation
'''
def plot_precipitation_bar_chart(city_id, start_date):
    conn = get_db_connection()
    if not conn: return
    cursor = conn.cursor()
    
    # 1. Get the City Name first
    city_name = get_city_name(cursor, city_id)

    # 2. Get the Weather Data
    query = """
    SELECT date, precipitation 
    FROM daily_weather_entries 
    WHERE city_id = ? AND date >= ? AND date <= date(?, '+6 days')
    """
    cursor.execute(query, (city_id, start_date, start_date))
    results = cursor.fetchall()
    conn.close()

    if not results:
        print(f"No data found for {city_name}.")
        return

    dates = [row[0] for row in results]
    precip = [row[1] for row in results]

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.bar(dates, precip, color='skyblue')
    plt.xlabel('Date')
    plt.ylabel('Precipitation (mm)')
    # UX IMPROVEMENT: Use the real name in the title
    plt.title(f'7-Day Precipitation for {city_name}') 
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

'''
2. Grouped Bar Chart: Min/Max/Mean Temperatures
'''
def plot_temp_stats_grouped_bar(city_id, start_date):
    conn = get_db_connection()
    if not conn: return
    cursor = conn.cursor()
    
    city_name = get_city_name(cursor, city_id)

    query = """
    SELECT date, min_temp, max_temp, mean_temp
    FROM daily_weather_entries
    WHERE city_id = ? AND date >= ? AND date <= date(?, '+4 days')
    """
    cursor.execute(query, (city_id, start_date, start_date))
    results = cursor.fetchall()
    conn.close()

    if not results:
        print(f"No data found for {city_name}.")
        return

    dates = [row[0] for row in results]
    min_temps = [row[1] for row in results]
    max_temps = [row[2] for row in results]
    mean_temps = [row[3] for row in results]

    x_indexes = range(len(dates))
    width = 0.25

    plt.figure(figsize=(10, 6))
    plt.bar([i - width for i in x_indexes], min_temps, width=width, label='Min Temp', color='blue')
    plt.bar([i for i in x_indexes], mean_temps, width=width, label='Mean Temp', color='orange')
    plt.bar([i + width for i in x_indexes], max_temps, width=width, label='Max Temp', color='red')

    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.title(f'Temperature Stats for {city_name}') # Real city name
    plt.xticks(ticks=x_indexes, labels=dates, rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()

'''
3. Multi-line Chart: Daily Min/Max Temperatures
'''
def plot_multi_line_temp(city_id, year):
    conn = get_db_connection()
    if not conn: return
    cursor = conn.cursor()
    
    city_name = get_city_name(cursor, city_id)

    query = """
    SELECT date, min_temp, max_temp 
    FROM daily_weather_entries 
    WHERE city_id = ? AND strftime('%Y', date) = ? AND strftime('%m', date) = '01'
    """
    cursor.execute(query, (city_id, str(year)))
    results = cursor.fetchall()
    conn.close()

    if not results:
        print(f"No data found for {city_name}.")
        return

    dates = [row[0] for row in results]
    min_temps = [row[1] for row in results]
    max_temps = [row[2] for row in results]

    plt.figure(figsize=(12, 6))
    plt.plot(dates, max_temps, label='Max Temp', color='red', marker='o')
    plt.plot(dates, min_temps, label='Min Temp', color='blue', marker='o')
    
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.title(f'Daily Min vs Max Temperature for {city_name} (Jan {year})') # Real Name
    plt.xticks(rotation=90)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

'''
4. Scatter Plot: Temperature vs Rainfall
'''
def plot_temp_vs_rain_scatter(city_id):
    conn = get_db_connection()
    if not conn: return
    cursor = conn.cursor()
    
    city_name = get_city_name(cursor, city_id)

    query = """
    SELECT mean_temp, precipitation 
    FROM daily_weather_entries 
    WHERE city_id = ?
    """
    cursor.execute(query, (city_id,))
    results = cursor.fetchall()
    conn.close()

    if not results:
        print(f"No data found for {city_name}.")
        return

    temps = [row[0] for row in results]
    rain = [row[1] for row in results]

    plt.figure(figsize=(10, 6))
    plt.scatter(temps, rain, alpha=0.5, color='green')
    
    plt.xlabel('Mean Temperature (°C)')
    plt.ylabel('Precipitation (mm)')
    plt.title(f'Correlation: Temp vs Rain for {city_name}')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    print("Generating Charts...")
    
    # 1. Bar Chart for City 1 
    plot_precipitation_bar_chart(city_id=1, start_date="2020-01-01")
    
    # 2. Grouped Bar Chart for City 
    plot_temp_stats_grouped_bar(city_id=1, start_date="2020-01-01")
    
    # 3. Multi-line Chart for City 
    plot_multi_line_temp(city_id=1, year="2020")
    
    # 4. Scatter Plot for City 
    plot_temp_vs_rain_scatter(city_id=1)