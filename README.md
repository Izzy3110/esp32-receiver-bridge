# esp32-receiver-device

## Description
Flask-App working as a bridge between Esp32 sending POST-Requests to the app. The app sends the received Data structured in a line-protocol format to an InfluxDB-Server Instance


## Status
### 2 working sensors simultaneously behind a i²c multiplexer

 - Adafruit TSL2591 High Dynamic Range Digital Light Sensor - STEMMA QT (https://www.adafruit.com/product/1980)
 - Adafruit BME688 - Temperature, Humidity, Pressure and Gas Sensor - STEMMA QT (https://www.adafruit.com/product/5046)

I²C Multiplexer Details:
 - Adafruit PCA9546 4-Channel STEMMA QT / Qwiic I2C Multiplexer - TCA9546A Compatible
(https://www.adafruit.com/product/5664)
