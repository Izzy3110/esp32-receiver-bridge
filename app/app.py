import asyncio
import base64
import json
import toml
import os
import threading
from wyl import config
from wyl.app import create_app
from wyl.logging import setup_logger

running = True

parsed_toml = toml.loads(open("config.toml").read())
toml_section: dict = parsed_toml.get("influx2")
toml_section_general: dict = parsed_toml.get("general")

app_host = toml_section_general.get("app_host")
app_port = toml_section_general.get("app_port")

logs_dir_basepath = os.path.join(os.path.dirname(__file__), "logs")
log_filepath = os.path.join(logs_dir_basepath, "debug.log")

config.influxdb_bucket = toml_section.get("bucket")
config.tz = toml_section_general.get("tz")
config.logs_dir_basepath = logs_dir_basepath
config.log_filepath = log_filepath
config.logger = setup_logger()
config.queue = asyncio.Queue()

if not os.path.isdir(logs_dir_basepath):
    os.makedirs(logs_dir_basepath, exist_ok=True)


app = create_app()


async def monitor_queue():
    while True:

        if config.queue.qsize() > 0:
            config.logger.debug("--- START DATA ---")
            while config.queue.qsize() > 0:
                item_ = await config.queue.get()
                json_data = json.loads(base64.b64decode(item_[0]).decode("utf-8"))
                config.logger.debug(json.dumps(json_data))
            config.logger.debug("--- END DATA ---")
            config.logger.debug("")

        await asyncio.sleep(5)


def run_asyncio_loop(loop_):
    asyncio.set_event_loop(loop_)
    loop_.run_forever()


def start_background_loop(loop_):
    t = threading.Thread(target=run_asyncio_loop, args=(loop_,))
    t.daemon = True
    t.start()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    start_background_loop(loop)
    asyncio.run_coroutine_threadsafe(monitor_queue(), loop)
    app.run(host=app_host, port=app_port, debug=True)
