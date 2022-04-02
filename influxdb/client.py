import os

from base.node import TEACHINGNode
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


class InfluxDBClientHandler:

    def __init__(self):
        self._host = os.environ['INFLUXDB_HOST']
        self._port = int(os.environ['INFLUXDB_PORT'])
        self._token = os.environ['INFLUXDB_TOKEN']
        self._org = os.environ['INFLUXDB_ORG']
        self._bucket = os.environ['INFLUXDB_BUCKET']

        self._client = None
        self._write_api = None
    
    @TEACHINGNode(producer=False, consumer=True)
    def __call__(self, input_fn):

        for msg in input_fn: 
            p = Point(msg.topic).field(msg.body.id, msg.body.value) # TODO: Specify the convention of messages
            self._write_api.write(bucket=self._bucket, record=p)

    def _build(self):
        self._client = InfluxDBClient(
            url=f'http://{self._host}:{self._port}', 
            token=self._token, 
            org=self._org
        )
        self._write_api = self._client.write_api(write_options=SYNCHRONOUS)