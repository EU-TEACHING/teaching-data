import os

from base.node import TEACHINGNode


def get_service_fn():
    SERVICE_TYPE = os.getenv('SERVICE_TYPE')
    produce, consume = False, True

    service_fns = []
    if SERVICE_TYPE == 'INFLUXDB':
        from influxdb import InfluxDBClientHandler
        host = os.getenv('INFLUXDB_HOST')
        port = int(os.getenv('INFLUXDB_PORT'))
        bucket =os.getenv('INFLUXDB_BUCKET')
        org = os.getenv('INFLUXDB_ORG')
        token = os.getenv('INFLUXDB_TOKEN')

        client = InfluxDBClientHandler(host, port, token, org, bucket)
        service_fns.append(client)
    
    return service_fns, produce, consume


if __name__ == '__main__':
    service_fn, produce, consume = get_service_fn()
    node = TEACHINGNode(service_fn, produce, consume)
    node.build()
    node.start()