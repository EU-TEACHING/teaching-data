from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


class InfluxDBClientHandler:

    def __init__(self, host, port, token, org, bucket):
        self._host = host
        self._port = port
        self._token = token
        self._org = org
        self._bucket = bucket

        self._client = InfluxDBClient(url=f'http://{host}:{port}', token=token, org=org)
        self._write_api = self._client.write_api(write_options=SYNCHRONOUS)
    
    def __call__(self, input_fn):

        while True:
            dp = next(input_fn)   
            p = Point(dp.topic).field(dp.body.id, dp.body.value) # Specify the convention
            self._write_api.write(bucket=self._bucket, record=p)
