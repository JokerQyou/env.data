# env.data
Data gathered by my main environment sensor.

# What
These data are gathered by my environment sensor using a BME280 sensor chip.
The sensor board is placed in my living room, facing the front door.

Folders are named in the format of `YYYYmm`, there are three JSON files in each of them, containing the temperature, air pressure, and (relative) humidity data of that month.

# How
The pipeline is as follows:

- the BME280 sensor is mounted on a NodeMCU board based on ESP8266.
- the board reads data from the sensor chip every 30 seconds, and sends to an MQTT server (over WiFi and over the Internet).
- A Python script is connected to the MQTT server as a client, it transfers the data into a statsd instance.
- A Graphite database stores all data passing into that statsd instance. It is also used for minimal visualization.
- the database is exported as JSON monthly, and converted to CSV files.

# Why
Well, why not?

# Caveats
- My sensor board runs 24/7, but will be missing data points from time to time, these might be caused by (not limited to):
  - Power outage
  - Network issue
  - Server maintenance
- the data of 2017.02 is for reference only. The firmware and the relay script of my sensor board was buggy at that time.
- Timestamps in these data files are UTC times, but I'm living in GMT+8 area.
- Data is uploaded every 30 seconds, but the exported data might be resampled to contain fewer data points.

# License
See LICENSE file for details.


