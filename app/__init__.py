import json

from flask import Flask, jsonify, request, Response, render_template
from flask_wtf.csrf import CSRFProtect
from influxdb_client import InfluxDBClient
from app.influx import token, org, bucket
from influxdb_client.client.write_api import SYNCHRONOUS


# Initialize
app = Flask(__name__)
# csrf = CSRFProtect()
# csrf.init_app(app)

# Config
app.config['DEBUG_MODE'] = True
app.config['SECRET_KEY'] = 'TheCureliestWalk'


# Routes
@app.route('/', methods=['GET', 'POST'])
def home():  # put application's code here
    return render_template('index.html')


@app.route('/get', methods=['GET'])
def getData():
    data = []
    with InfluxDBClient(url="http://10.101.118.91:8086", token=token, org=org) as client:
        query = 'from(bucket: "{}") |> range(start: -1h)'.format(bucket)
        tables = client.query_api().query(query, org=org)
        for table in tables:
            for i, record in enumerate(table.records):
                # Print on console
                # print(record["_measurement"], record["_field"], record["_value"])
                # measurement.append(record["_measurement"])
                # field.append(record["_field"])
                # value.append(record["_value"])
                data.append({ "id": i, "_measurement": record["_measurement"], "_field": record["_field"], '_value': record["_value"], "timestamp": record["_time"]})
        client.close()
        return jsonify(data)


@app.route('/<measurement>/<data_key>/<data_value>/<field_key>/<field_value>', methods=['POST'])
def writeData(measurement, data_key, data_value, field_key, field_value):
    # measurement = "flask_app"
    # data_key = "location"
    # data_value = 1
    # field_key = "last_speed_record"
    # field_value = 48

    measurement = request.view_args['measurement']
    data_key = request.view_args['data_key']
    data_value = request.view_args['data_value']
    field_key = request.view_args['field_key']
    field_value = request.view_args['field_value']

    with InfluxDBClient(url="http://10.101.118.91:8086", token=token, org=org) as client:
        write_api = client.write_api(write_options=SYNCHRONOUS)
        # "measurement,data _field"
        data = f"{measurement},{data_key}={data_value} {field_key}={field_value}"
        # -------------------------^------------- index of location 1: ex. "Kang Sa Dan"
        write_api.write(bucket, org, data)
        client.close()
    return jsonify({"message": "Data write successfully!"}), 200