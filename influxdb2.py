import time
from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from private_info import token
from private_info import org
from private_info import bucket
from private_info import DB_url

client2 = InfluxDBClient(url=DB_url, token=token)

write_api = client2.write_api(write_options=SYNCHRONOUS)

p = Point("hue_temperature").tag("sensor","ground_floor").field("temperature",25.3)
p2 = Point("hue_temperature").tag("sensor","ground_floor").field("temperature2",15.3)
write_api.write(bucket=bucket, org=org, record=[p, p2])

