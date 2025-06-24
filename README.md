# esp32-receiver-device

## Description
Flask-App working as a bridge between Esp32 sending POST-Requests to the app. The app sends the received Data structured in a line-protocol format to an InfluxDB-Server Instance

## Used Hardware
 - Adafruit QT Py ESP32-S2 (including uFL version) (https://www.adafruit.com/product/5348)

## Used Software

### App
 - Docker Image - python:3.10

### Python Modules
 - Flask 3.0.3
 - influxdb-client 1.46.0

### Devices
 - CircuitPython 9.2.8 (https://circuitpython.org/board/adafruit_qtpy_esp32s2/)


## Status
### 2 working sensors simultaneously behind a i²c multiplexer

 - Adafruit TSL2591 High Dynamic Range Digital Light Sensor - STEMMA QT (https://www.adafruit.com/product/1980)
 - Adafruit BME688 - Temperature, Humidity, Pressure and Gas Sensor - STEMMA QT (https://www.adafruit.com/product/5046)

I²C Multiplexer Details:
 - Adafruit PCA9546 4-Channel STEMMA QT / Qwiic I2C Multiplexer - TCA9546A Compatible
(https://www.adafruit.com/product/5664)
