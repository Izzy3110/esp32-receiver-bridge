import base64
import json
import uuid
from flask import Blueprint, jsonify, request

from wyl import config
from wyl.helpers import localize_datetime
from wyl.influx import send_sensor_to_influx
from wyl.line_protocol import json_device_to_line_protocol, json_to_line_protocol

bp_data = Blueprint("data", __name__)


@bp_data.route("/")
async def health():
    return jsonify({})


@bp_data.route("/device-id", methods=["GET"])
async def device_id():
    return jsonify({"device_id": uuid.uuid4()})


@bp_data.route("/device", methods=["POST"])
async def device_data():
    device_id_ = request.form.get("device_id")
    sensors_list = json.loads(request.form.get("sensors"))

    sensors_dict = {}
    k = 0
    for sensor in sensors_list:
        key_ = f"sensor_{k}"
        sensors_dict[key_] = sensor
        k += 1

    json_device_data = {
        "device_id": device_id_,
        "sensor_list": sensors_dict,
        "sensor_datetime": localize_datetime(request.form.get("datetime")),
    }

    line_protocol_data = json_device_to_line_protocol(json_device_data)

    config.logger.debug(line_protocol_data)
    await send_sensor_to_influx(line_protocol_data)
    return jsonify(json_device_data)


@bp_data.route("/sensor-post", methods=["POST"])
async def sensor_post():
    dt = request.form.get("datetime")
    # print(request.form.keys())
    # data = request.form.get('data')
    # sensor = request.form.get('sensor')
    device_id_ = request.form.get("device_id")

    sensor_name = request.form.get("sensor")
    sensor_data = request.form.get("data")

    json_data = {
        "device_id": device_id_,
        "sensor_name": sensor_name,
        "sensor_data": json.loads(sensor_data),
        "sensor_datetime": localize_datetime(dt),
    }

    line_protocol_data = json_to_line_protocol(json_data)
    config.logger.debug(f"data: {line_protocol_data}")

    await send_sensor_to_influx(line_protocol_data)

    """
    await config.queue.put(
        (base64.b64encode(json.dumps(json_data).encode("utf-8")).decode("utf-8"),)
    )
    config.logger.debug(f"qsize: {config.queue.qsize()}")
    """

    return jsonify({"success": True})
