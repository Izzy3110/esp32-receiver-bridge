from influxdb_client.client.influxdb_client_async import InfluxDBClientAsync


async def send_sensor_to_influx(bucket, line_protocol_data):
    async with InfluxDBClientAsync.from_config_file('config.toml') as async_write_client:
        await async_write_client.write_api().write(bucket=bucket, record=line_protocol_data)
