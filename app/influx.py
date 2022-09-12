from datetime import datetime
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

class InfluxUp():
    def __init__(self):
        self.token = "u4PvOC7Pm0wCHZSy2q-yZgRTkRN1OY-p42OTKQeAgw0tmjs29cjCrDEuzSwafE8-TLEOIdcgKkTJR873kdiHzA=="
        self.org = "kkuiot"
        self.bucket = "iho"
        # Data
        self.measurement = "flask_app"
        self.data_key = "location"
        self.data_value = 1
        self.field_key = "last_speed_record"
        self.field_value = 48

        with InfluxDBClient(url="http://10.101.118.91:8086", token=self.token, org=self.org) as self.client:
            self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
            # "measurement,data _field"
            self.data = f"{self.measurement},{self.data_key}={self.data_value} {self.field_key}={self.field_value}"
            # -------------------------^------------- index of location 1: ex. "Kang Sa Dan"
            self.write_api.write(self.bucket, self.org, self.data)

            # Query

            self.query = 'from(bucket: "iho") |> range(start: -1m)'
            self.tables = self.client.query_api().query(self.query, org=self.org)
            for table in self.tables:
                for record in table.records:
                    print(record["_measurement"], record["_field"], record["_value"])
            self.client.close()

# calling for class
init = InfluxUp()