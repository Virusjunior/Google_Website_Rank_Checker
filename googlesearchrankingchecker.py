import requests    
from bs4 import BeautifulSoup
import psycopg2
from datetime import datetime


# Connect to the PostgreSQL database 
# add hostname, database name, user,password for your database to connect to it. port is 5432 by default
conn = psycopg2.connect(host="db_hostname", dbname="db_name", user="db_user_name", password="db_ps", port="5432")
cur = conn.cursor()

# Create table if not exists
cur.execute("""
    CREATE TABLE IF NOT EXISTS website_rankings (
        id SERIAL PRIMARY KEY,
        keyword VARCHAR(255),
        url VARCHAR(255),
        ranking INTEGER,
        date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
""")
conn.commit()

# Define function to get Google search results
def get_google_results(query):
    res = requests.get(f"https://www.google.com/search?q={query}")
    soup = BeautifulSoup(res.text, "html.parser")
    results = []
    for i, link in enumerate(soup.find_all("a")):
        href = link.get("href")
        if href.startswith("/url?q="):
            href = href.split("/url?q=")[1].split("&")[0]
            results.append(href)
    return results

# Define function to get ranking for a URL and keyword
def get_ranking(keyword, url):
    results = get_google_results(keyword)
    for i, result in enumerate(results):
        if url in result:
            return i + 1
    return -1

# Example usage
keyword = "postgresql schema"
url = "https://www.javatpoint.com/postgresql-schema"
ranking = get_ranking(keyword, url)

# Insert ranking data into table
cur.execute("""
    INSERT INTO website_rankings (keyword, url, ranking)
    VALUES (%s, %s, %s);
""", (keyword, url, ranking))
conn.commit()

# Select all data from table and print results
cur.execute("SELECT * FROM website_rankings")
rows = cur.fetchall()
for row in rows:
    print(row)

# Close database connection
cur.close()
conn.close()















