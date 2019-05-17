# env.data
Data gathered by my main environment sensor.

# What
These data are gathered by my environment sensor using a BME280 sensor chip.
The sensor board is placed in my living room, facing the front door.

Folders are named in the format of `YYYY/mm`, there are three JSON files in each of them, containing the temperature, air pressure, and (relative) humidity data of that month.

# How

The pipeline used to work like this (before 2018/09):

- The BME280 sensor is mounted on a NodeMCU board based on ESP8266.
- The board reads data from the sensor chip every 30 seconds, and sends to an MQTT server (over WiFi).
- A Python script is connected to the MQTT server as a client, it transfers the data into a statsd instance.
- A Graphite database stores all data passing into that statsd instance. It is also used for minimal visualization.
- Data is exported as JSON monthly, and converted to CSV files.

The current pipeline works like this (since 2018/09):

- The BME280 sensor is mounted on a NodeMCU board based on ESP8266.
- The board reads data from the sensor and send them to LeanCloud (over WiFi).
- The board goes into deepsleep mode to save energy. A rewake signal would be set so the board can rewake itself to capture data every 10 minutes.
- Data is exported as CSV files monthly.

# Why
Well, why not?

# Units

- Temperature: Celsius;
- Pressure: hPa, in which 1hPa equals 100Pa;

# Caveats
- My sensor board runs 24/7, but date points will be missing from time to time in case of:
  - Power outage
  - Network issue
  - Server maintenance
- These data files are missing too many data points:
  - `2017/02`: the sensor board firmware and relay script was buggy when I first set them up.
  - `2018/09`: I switched from selfhosted MQTT-statsd-prometheus-grafana instance to LeanCloud storage.
- No need to say, timestamps are in UTC, but I live in GMT+8 region.
- Resolution:
  - Before 2018/09, data was captured every 30 seconds, and resampled by Grafana when exporting to CSV files.
  - Since 2018/09, data was captured every 10 minutes, and exported as is.

# License
See LICENSE file for details.

