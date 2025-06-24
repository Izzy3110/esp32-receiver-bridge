import sys

import serial
import time
import logging
import requests

logging.basicConfig(filename="serial.log", encoding="UTF-8", filemode="a", format='%(asctime)s.%(msecs)03d '
                                '%(filename)s: '    
                                '%(levelname)s: '
                                '%(funcName)s(): '
                                '%(lineno)d:\t'
                                '%(message)s',datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger("serial")
logger.setLevel(logging.DEBUG)


def connect_to_serial(port, baud_rate):
    try:
        # Open the serial port
        ser = serial.Serial(port, baud_rate, timeout=1)
        logger.debug("Serial port connected successfully.")
        return ser
    except serial.SerialException as e:
        logger.error(f"Error: {e}")
        return None


def main(com_port, baud_rate=115200):
    while True:
        ser = connect_to_serial(com_port, baud_rate)
        if ser:
            try:
                while True:
                    try:
                        line = ser.readline().decode().strip()
                    except serial.serialutil.SerialException:
                        break
                    except UnicodeDecodeError:
                        pass
                    except KeyboardInterrupt:
                        sys.exit(0)
                    if len(line.strip()) > 0:
                        """
                        resp = requests.post('http://192.168.137.64:3003/serial-in', json=
                        {
                            "port": port,
                            "baud_rate": baud_rate,
                            "message": line,
                            "time": time.time()
                        })
                        print(resp.json())
                        """
                        print(line)
                        logger.info(f"Received: {line}")

            except serial.SerialException as e:
                logger.error("Error:", e)
            finally:
                # Close the serial port
                ser.close()
                logger.debug("Serial port closed.")
        logger.debug("Restarting in 3 seconds...")

        time.sleep(3)


if __name__ == "__main__":
    port = sys.argv[1]
    main(port)
