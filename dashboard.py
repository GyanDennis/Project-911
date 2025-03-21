import sqlite3
import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px
from flask import Flask

# Flask server
server = Flask(__name__)
app = dash.Dash(__name__, server=server)

DB_FILE = "threats.db"

def fetch_threat_data():
"""Retrieve stored threats from the database."""
conn = sqlite3.connect(DB_FILE)
df = pd.read_sql_query("SELECT * FROM threats", conn)
conn.close()
return df

app.layout = html.Div([
html.H1("🚨 Project 911 - Real-Time Threat Monitoring"),

dcc.Interval(id="update_interval", interval=5000, n_intervals=0),  # Refresh every 5 sec

html.Div([
html.H3("Threat Map"),
dcc.Graph(id="threat_map")
]),

html.Div([
html.H3("Threat Frequency Over Time"),
dcc.Graph(id="threat_trend")
]),

html.Div([
html.H3("Threats by Sensor Type"),
dcc.Graph(id="threat_sensor_chart")
])
])

@app.callback(
[dash.Output("threat_map", "figure"),
dash.Output("threat_trend", "figure"),
dash.Output("threat_sensor_chart", "figure")],
dash.Input("update_interval", "n_intervals")
)
def update_dashboard(n):
"""Fetch latest threats and update dashboard."""
df = fetch_threat_data()
if df.empty:
return px.scatter_mapbox(lat=[], lon=[], zoom=3), px.line(), px.bar()

map_fig = px.scatter_mapbox(df, lat="latitude", lon="longitude", color="threat_level",
size_max=10, zoom=3, mapbox_style="open-street-map",
title="Live Threat Locations")

df["timestamp"] = pd.to_datetime(df["timestamp"])
trend_fig = px.line(df.groupby(df["timestamp"].dt.minute).size().reset_index(name="count"),
x="timestamp", y="count",
title="Threat Frequency Over Time")

sensor_fig = px.bar(df.groupby("sensor_type").size().reset_index(name="count"),
x="sensor_type", y="count",
title="Threats by Sensor Type")

return map_fig, trend_fig, sensor_fig

if __name__ == "__main__":
app.run_server(debug=True, port=8050)
