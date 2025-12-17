import sys
sys.stdout = sys.__stdout__
import sqlite3
import matplotlib.pyplot as plt

DB_FILE = "CIS4044-N-SDI-OPENMETEO-PARTIAL.db"

def get_db_connection():
    try:
        return sqlite3.connect(DB_FILE)
    except sqlite3.Error as e:
        print(e)
        return None

'''
ADVANCED ANALYSIS 1: Seasonal Comparison
'''
def plot_all_cities_monthly_temp_comparison(year):
    conn = get_db_connection()
    if not conn: return
    cursor = conn.cursor()

    query = """
    SELECT cities.name, strftime('%m', date) as month, AVG(mean_temp)
    FROM daily_weather_entries
    JOIN cities ON daily_weather_entries.city_id = cities.id
    WHERE strftime('%Y', date) = ?
    GROUP BY cities.name, month
    ORDER BY cities.name, month
    """
    
    cursor.execute(query, (str(year),))
    results = cursor.fetchall()
    conn.close()

    if not results:
        print("No data found for seasonal analysis.")
        return

    city_data = {}
    for row in results:
        city = row[0]
        temp = row[2]
        
        ### FIX: Handle None values if a month has no data
        if temp is None: temp = 0 
        
        if city not in city_data:
            city_data[city] = []
        city_data[city].append(temp)

    plt.figure(figsize=(12, 7))
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    for city, temps in city_data.items():
        # Ensure x and y match length
        current_months = months[:len(temps)] 
        plt.plot(current_months, temps, marker='o', label=city)

    plt.xlabel('Month')
    plt.ylabel('Average Monthly Temperature (°C)')
    plt.title(f'Seasonal Climate Comparison ({year})')
    plt.legend()
    plt.grid(True)
    plt.show()

'''
ADVANCED ANALYSIS 2: Weather Volatility Index
'''
def plot_temperature_volatility_comparison():
    conn = get_db_connection()
    if not conn: return
    cursor = conn.cursor()

    query = """
    SELECT cities.name, AVG(max_temp - min_temp) as volatility
    FROM daily_weather_entries
    JOIN cities ON daily_weather_entries.city_id = cities.id
    GROUP BY cities.name
    ORDER BY volatility DESC
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()

    # Filter out None values
    clean_results = [row for row in results if row[1] is not None]
    
    if not clean_results:
        print("Not enough data for volatility analysis.")
        return

    cities = [row[0] for row in clean_results]
    volatility = [row[1] for row in clean_results]

    plt.figure(figsize=(10, 6))
    bars = plt.bar(cities, volatility, color='purple', alpha=0.7)
    
    plt.xlabel('City')
    plt.ylabel('Avg Daily Temp Swing (°C)')
    plt.title('Climate Stability Index (Lower is More Stable)')
    plt.bar_label(bars, fmt='%.1f°C')
    plt.show()

'''
ADVANCED ANALYSIS 3: Rainfall Pattern Analysis
'''
def plot_rain_pattern_scatter():
    conn = get_db_connection()
    if not conn: return
    cursor = conn.cursor()

    # Query: Count rainy days (>0.1mm) AND Average rain amount on those days
    query = """
    SELECT 
        cities.name, 
        COUNT(CASE WHEN precipitation > 0.1 THEN 1 END) as rainy_days,
        AVG(CASE WHEN precipitation > 0.1 THEN precipitation END) as rain_intensity
    FROM daily_weather_entries
    JOIN cities ON daily_weather_entries.city_id = cities.id
    GROUP BY cities.name
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()

    if not results: return

    # Prepare lists
    cities = []
    days = []
    intensity = []

    for row in results:
        city_name = row[0]
        r_days = row[1]
        r_int = row[2]

        ### FIX: CRITICAL ERROR PREVENTION
        # If it never rained (r_days = 0), then r_int will be None (division by zero in SQL).
        # We must replace None with 0.0 to prevent Matplotlib crash.
        if r_int is None:
            r_int = 0.0
        
        cities.append(city_name)
        days.append(r_days)
        intensity.append(r_int)

    plt.figure(figsize=(10, 6))
    plt.scatter(days, intensity, s=100, c='blue', alpha=0.6, edgecolors='black')

    # Annotate each dot with the city name
    for i, city in enumerate(cities):
        # This is where your code was crashing (coordinate cannot be None)
        plt.annotate(city, (days[i], intensity[i]), xytext=(5, 5), textcoords='offset points')

    plt.xlabel('Number of Rainy Days (Frequency)')
    plt.ylabel('Avg Rain per Rainy Day (Intensity in mm)')
    plt.title('Rainfall Analysis: Drizzly vs Stormy Cities')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    # Note: Ensure you check a year where data actually exists!
    # If 2020 has no data for new cities, try 2024.
    print("Running Advanced Analysis...")
    plot_all_cities_monthly_temp_comparison(2024) 
    plot_temperature_volatility_comparison()
    plot_rain_pattern_scatter()