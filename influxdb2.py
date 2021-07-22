import time
from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# You can generate a Token from the "Tokens Tab" in the UI
token = "ze0ElzHkrPlZsXUUeG_UCiRZRtdG3IAVWLSN7RRgFKUhJqQjmRrO_J0Oh8sFi9dehPpx8QjJ3ff_bnjndK_Ulg=="
org = "cvs"
bucket = "localdatadb2"

client2 = InfluxDBClient(url="http://localhost:8086", token=token)

write_api = client2.write_api(write_options=SYNCHRONOUS)

for i in range(10):
    p = Point("hue_temperature").tag("sensor","ground_floor").field("temperature",25.3 + i*i)
    p2 = Point("hue_temperature").tag("sensor","ground_floor").field("temperature2",15.3 + i*i)
    write_api.write(bucket=bucket, org=org, record=[p, p2])
    print(i)
    time.sleep(10)

