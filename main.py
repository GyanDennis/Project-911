import asyncio
import websockets
import json
from geopy.distance import geodesic
import database
import alerts
from datetime import datetime

# Base location (HQ coordinates)
BASE_LATITUDE = 37.7749
BASE_LONGITUDE = -122.4194
DETECTION_RANGE = 300  # in KM

async def receive_sensor_data():
"""Receives live sensor data from WebSocket."""
async with websockets.connect("ws://localhost:8765") as websocket:
while True:
message = await websocket.recv()
data = json.loads(message)
process_data(data)

def calculate_distance(threat_lat, threat_lon):
"""Calculate distance from base location."""
base_location = (BASE_LATITUDE, BASE_LONGITUDE)
threat_location = (threat_lat, threat_lon)
return geodesic(base_location, threat_location).kilometers

def process_data(data):
"""Process sensor data, check for threats, store, and send alerts."""
distance = calculate_distance(data["latitude"], data["longitude"])

if distance <= DETECTION_RANGE and data["threat_level"] == "High":
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
threat_message = f"⚠️ HIGH THREAT DETECTED!\nSensor: {data['sensor_type']}\nLocation: {data['latitude']}, {data['longitude']}\nDistance: {distance:.2f} km\nTime: {timestamp}"

print(threat_message)

# Store in database
database.store_threat(data["latitude"], data["longitude"], data["sensor_type"], data["threat_level"], distance, timestamp)

# Send Alerts
alerts.send_email_alert(threat_message)
alerts.send_sms_alert(threat_message)

if __name__ == "__main__":
print("🔍 Project 911 - Threat Detection System Running...")
asyncio.run(receive_sensor_data())
