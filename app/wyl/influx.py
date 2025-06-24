import os

from influxdb_client.client.influxdb_client_async import InfluxDBClientAsync


async def send_sensor_to_influx(line_protocol_data):
    bucket = os.getenv('INFLUXDB_BUCKET')
    async with InfluxDBClientAsync.from_config_file(
        "config.toml"
    ) as async_write_client:
        await async_write_client.write_api().write(
            bucket=bucket, record=line_protocol_data
        )
