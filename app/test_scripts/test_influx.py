import asyncio
import os
from datetime import datetime
from influxdb_client.client.influxdb_client_async import InfluxDBClientAsync
import toml

parsed_toml = toml.loads(open("config.toml").read())
toml_section: dict = parsed_toml.get("influx2")
toml_section_general: dict = parsed_toml.get("general")

bucket = toml_section.get("bucket")
url = toml_section.get("url")
token = toml_section.get("token")
org = toml_section.get("org")

tz = toml_section_general.get("tz")


# Function to format the field value correctly
def format_value(value):
    if isinstance(value, str):
        return f'"{value}"'
    elif isinstance(value, bool):
        return str(value).lower()
    else:
        return value


def json_to_line_protocol(data):
    measurement = "sensor_data"
    tags = f"device_id={data['device_id']},sensor_name={data['sensor_name']}"
    fields = ",".join(
        [f"{k}={format_value(v)}" for k, v in data["sensor_data"].items()]
    )
    timestamp = int(
        datetime.fromisoformat(data["sensor_datetime"]).timestamp() * 1e9
    )  # InfluxDB expects nanoseconds
    line_protocol = f"{measurement},{tags} {fields} {timestamp}"
    return line_protocol


async def send_sensor_to_influx(line_protocol_data):
    async with InfluxDBClientAsync.from_config_file(
        "config.toml"
    ) as async_write_client:
        await async_write_client.write_api().write(
            bucket=bucket, record=line_protocol_data
        )


async def query():
    async with InfluxDBClientAsync.from_config_file("config.toml") as client:
        tables = await client.query_api().query(
            f'from(bucket:"{bucket}") |> range(start: -5m)'
        )
        for value in tables.to_values(columns=["device_id", "_time", "_value"]):
            print(value)


data_json = {
    "device_id": "test_device",
    "sensor_name": "test_sensor",
    "sensor_data": {"temperature": 0.0},
    "sensor_datetime": datetime.now().isoformat(),
}


async def main():
    await send_sensor_to_influx(json_to_line_protocol(data_json))
    await asyncio.sleep(3)
    await query()


if __name__ == "__main__":
    asyncio.run(main())
