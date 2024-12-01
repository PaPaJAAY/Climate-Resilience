import re
import json
import socket
import urllib.request
import sqlite3
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

# === PART 1: Data Collection and Web Scraping ===

# Function to fetch JSON data from a weather API (replace with actual climate data URL)
def fetch_climate_data(url):
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode("utf-8"))
        return data
    except urllib.error.URLError as e:
        print(f"Error fetching climate data: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON data: {e}")
        return None

# Function to fetch news articles related to climate (replace with actual news URL)
def fetch_news_articles(url):
    try:
        with urllib.request.urlopen(url) as response:
            html = response.read().decode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        articles = []
        for item in soup.select("article"):
            title = item.find("h2").get_text()
            link = item.find("a")["href"]
            articles.append({"title": title, "link": link})
        return articles
    except urllib.error.URLError as e:
        print(f"Error fetching news articles: {e}")
        return []
    except AttributeError as e:
        print(f"Error parsing HTML content: {e}")
        return []

# Function to save fetched data to JSON file
def save_to_json(data, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"Error saving data to {filename}: {e}")

# === PART 2: Database Setup and Data Insertion ===

# Function to initialize database and create tables
def setup_database():
    try:
        conn = sqlite3.connect('climate_risk.db')
        cursor = conn.cursor()
        
        # Creating tables for climate data, news articles, users, and projects
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS ClimateData (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            temperature REAL,
            humidity REAL,
            date TEXT,
            location TEXT
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS NewsArticles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            link TEXT,
            date TEXT
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Enrollments (
            user_id INTEGER,
            project_id INTEGER,
            PRIMARY KEY (user_id, project_id),
            FOREIGN KEY (user_id) REFERENCES Users(id),
            FOREIGN KEY (project_id) REFERENCES Projects(id)
        )
        ''')
        
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database setup error: {e}")
    finally:
        conn.close()

# Function to insert climate data into the database
def insert_climate_data(temperature, humidity, date, location):
    try:
        conn = sqlite3.connect('climate_risk.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO ClimateData (temperature, humidity, date, location) VALUES (?, ?, ?, ?)",
                       (temperature, humidity, date, location))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error inserting climate data: {e}")
    finally:
        conn.close()

# Function to insert news articles into the database
def insert_news_article(title, link, date):
    try:
        conn = sqlite3.connect('climate_risk.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO NewsArticles (title, link, date) VALUES (?, ?, ?)",
                       (title, link, date))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error inserting news article: {e}")
    finally:
        conn.close()

# === PART 3: Data Serialization ===

# Function to serialize data to JSON
def serialize_to_json(data, filename):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"Error serializing data to {filename}: {e}")

# Function to deserialize data from JSON
def deserialize_from_json(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except IOError as e:
        print(f"Error reading from {filename}: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {filename}: {e}")
        return None

# === PART 4: Data Visualization ===

# Function to fetch climate data from the database for visualization
def fetch_climate_data_for_visualization():
    try:
        conn = sqlite3.connect('climate_risk.db')
        cursor = conn.cursor()
        cursor.execute("SELECT date, temperature FROM ClimateData")
        data = cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error fetching climate data: {e}")
        return []
    finally:
        conn.close()
    return data

# Function to visualize climate data over time
def visualize_climate_data():
    data = fetch_climate_data_for_visualization()
    if not data:
        print("No data available for visualization.")
        return

    dates = [row[0] for row in data]
    temperatures = [row[1] for row in data]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, temperatures, marker='o')
    plt.title('Temperature Over Time')
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# === PART 5: Main Function to Run the Project ===

def main():
    # Initialize the database
    setup_database()

    # Collect and save climate data (replace with actual climate data URL)
    climate_data = fetch_climate_data("https://jsonplaceholder.typicode.com/todos/1")  # Example placeholder URL
    if climate_data:
        save_to_json(climate_data, "climate_data.json")
    
        # Insert example climate data into the database
        insert_climate_data(25.3, 60, "2024-11-07", "San Francisco")
    
    # Collect and save news articles (replace with actual news URL)
    news_articles = fetch_news_articles("https://example.com/climate-news")  # Example placeholder URL
    for article in news_articles:
        insert_news_article(article["title"], article["link"], "2024-11-07")  # Replace date as needed
    save_to_json(news_articles, "news_articles.json")

    # Serialize climate data to JSON
    serialize_to_json(climate_data, 'climate_serialized.json')
    
    # Visualize climate data from the database
    visualize_climate_data()

# Run the main function
if __name__ == "__main__":
    main()
