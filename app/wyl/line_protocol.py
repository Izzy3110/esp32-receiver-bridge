from datetime import datetime

from wyl.helpers import format_value


def json_device_to_line_protocol(data):
    measurement = "sensor_devices"
    tags = f"device_id={data['device_id']},list=sensors"
    fields = ",".join(
        [f"{k}={format_value(v)}" for k, v in data["sensor_list"].items()]
    )
    timestamp = int(
        datetime.fromisoformat(data["sensor_datetime"]).timestamp() * 1e9
    )  # InfluxDB expects nanoseconds
    line_protocol = f"{measurement},{tags} {fields} {timestamp}"
    return line_protocol


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
