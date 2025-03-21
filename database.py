mport sqlite3

DB_FILE = "threats.db"

def initialize_db():
"""Create a database for storing threats."""
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS threats (
id INTEGER PRIMARY KEY AUTOINCREMENT,
latitude REAL,
longitude REAL,
sensor_type TEXT,
threat_level TEXT,
distance_km REAL,
timestamp TEXT
)
""")
conn.commit()
conn.close()

def store_threat(latitude, longitude, sensor_type, threat_level, distance_km, timestamp):
"""Save detected threats in the database."""
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()
cursor.execute("""
INSERT INTO threats (latitude, longitude, sensor_type, threat_level, distance_km, timestamp)
VALUES (?, ?, ?, ?, ?, ?)
""", (latitude, longitude, sensor_type, threat_level, distance_km, timestamp))
conn.commit()
conn.close()

def fetch_threats():
"""Retrieve all stored threats."""
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()
cursor.execute("SELECT * FROM threats")
threats = cursor.fetchall()
conn.close()
return threats

# Initialize the database
initialize_db()
