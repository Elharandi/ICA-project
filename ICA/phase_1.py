# Author: <Your name here>
# Student ID: <Your Student ID>

import sqlite3

# Phase 1 - Starter
# 
# Note: Display all real/float numbers to 2 decimal places.

'''
Satisfactory 50-59
'''
def select_all_countries(connection):
    # Queries the database and selects all the countries 
    # stored in the countries table of the database.
    # The returned results are then printed to the 
    # console.
    try:
        # Define the query
        query = "SELECT * from [countries]"

        # Get a cursor object from the database connection
        # that will be used to execute database query.
        cursor = connection.cursor()

        # Execute the query via the cursor object.
        results = cursor.execute(query)

        # Iterate over the results and display the results.
        print(f"\n--- All Countries ---")
        for row in results:
            # row[0] is id, row[1] is name, row[2] is timezone
            print(f"Country Id: {row[0]} -- Country Name: {row[1]} -- Country Timezone: {row[2]}")

    except sqlite3.OperationalError as ex:
        print(ex)

def select_all_cities(connection):
    try:
        query = "SELECT * from [cities]"
        cursor = connection.cursor()
        results = cursor.execute(query)

        print(f"\n--- All Cities ---")
        for row in results:
            print(f"City Id: {row[0]} -- City Name: {row[1]} -- Country Id: {row[2]} -- Lat/Long: {row[3]}")

    except sqlite3.OperationalError as ex:
        print(ex)

'''
Good
'''
def average_annual_temperature(connection, city_id, year):
    try:
        cursor = connection.cursor()
        
        #filtering by city_id AND the year part of the date column
        query = """
        SELECT AVG(mean_temp) 
        FROM daily_weather_entries 
        WHERE city_id = ? AND strftime('%Y', date) = ?
        """
        
        #parameters passed safely as a tuple
        cursor.execute(query, (city_id, str(year)))
        result = cursor.fetchone()

        print(f"\n--- Average Temperature for City ID {city_id} in {year} ---")
        if result and result[0] is not None:
            print(f"Average Mean Temp: {result[0]:.2f} C")
        else:
            print("No data found for this city/year combination.")

    except sqlite3.OperationalError as ex:
        print(ex)

def average_seven_day_precipitation(connection, city_id, start_date):
    try:
        cursor = connection.cursor()
        
        query = """
        SELECT AVG(precipitation) 
        FROM daily_weather_entries 
        WHERE city_id = ? AND date >= ? AND date <= date(?, '+6 days')
        """
        
        cursor.execute(query, (city_id, start_date, start_date))
        result = cursor.fetchone()

        print(f"\n--- 7-Day Average Precipitation (Start: {start_date}) ---")
        if result and result[0] is not None:
            print(f"Average Precipitation: {result[0]:.2f} mm")
        else:
            print("No data found for this period.")

    except sqlite3.OperationalError as ex:
        print(ex)

'''
Very Good
'''
def average_mean_temp_by_city(connection, date_from, date_to):
    try:
        cursor = connection.cursor()
        
        # Joining cities with weather entries to get the City Name instead of just ID
        query = """
        SELECT cities.name, AVG(daily_weather_entries.mean_temp) 
        FROM daily_weather_entries 
        JOIN cities ON daily_weather_entries.city_id = cities.id
        WHERE date BETWEEN ? AND ?
        GROUP BY cities.name
        """
        
        cursor.execute(query, (date_from, date_to))
        results = cursor.fetchall()

        print(f"\n--- Average Mean Temp by City ({date_from} to {date_to}) ---")
        for row in results:
            print(f"City: {row[0]} -- Average Temp: {row[1]:.2f} C")

    except sqlite3.OperationalError as ex:
        print(ex)

def average_annual_precipitation_by_country(connection, year):
    try:
        cursor = connection.cursor()
        
        #Joining Country to City and Weather
        query = """
        SELECT countries.name, AVG(daily_weather_entries.precipitation)
        FROM daily_weather_entries
        JOIN cities ON daily_weather_entries.city_id = cities.id
        JOIN countries ON cities.country_id = countries.id
        WHERE strftime('%Y', date) = ?
        GROUP BY countries.name
        """
        
        cursor.execute(query, (str(year),))
        results = cursor.fetchall()

        print(f"\n--- Average Daily Precipitation by Country ({year}) ---")
        for row in results:
            print(f"Country: {row[0]} -- Average Daily Rain: {row[1]:.2f} mm")

    except sqlite3.OperationalError as ex:
        print(ex)

if __name__ == "__main__":
    # Create a SQLite3 connection and call the various functions
    db_file = "CIS4044-N-SDI-OPENMETEO-PARTIAL.db" 
    
    try:
        conn = sqlite3.connect(db_file)
        print("Connected to database successfully.\n")

       
        select_all_countries(conn)
        select_all_cities(conn)

      
        # Using City ID 1 and Year 2020 based on DB data
        average_annual_temperature(conn, 1, "2020") 
        average_seven_day_precipitation(conn, 1, "2020-01-01")

       
        average_mean_temp_by_city(conn, "2020-01-01", "2020-12-31")
        average_annual_precipitation_by_country(conn, "2020")

        conn.close()
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")