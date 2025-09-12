""" Module to take a water_level reading."""

# Raspi-sump, a sump pump monitoring system.
# Al Audet
# https://www.linuxnorth.org/raspi-sump/
#
# All configuration changes should be done in raspisump.conf
# MIT License -- https://www.linuxnorth.org/raspi-sump/license.html

#from hcsr04sensor import sensor
import vl53l1x
from raspisump import log, alerts, heartbeat, config_values

configs = config_values.configuration()


def initiate_heartbeat():
    """Initiate the heartbeat email process if needed"""
    if configs["heartbeat"] == 1:
        heartbeat.determine_if_heartbeat()
    else:
        pass


def water_reading():
    """Initiate a water level reading."""
    pit_depth = configs["pit_depth"]
#    trig_pin = configs["trig_pin"]
#    echo_pin = configs["echo_pin"]
#    temperature = configs["temperature"]
#    unit = configs["unit"]

#    value = sensor.Measurement(trig_pin, echo_pin, temperature, unit)
#   Open and start the VL53L1X sensor.
#   If you've previously used change-address.py then you
#   should use the new i2c address here.
#   If you're using a software i2c bus (ie: HyperPixel4) then
#   you should `ls /dev/i2c-*` and use the relevant bus number.
    tof = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x29)
    tof.open()

#   Optionally set an explicit timing budget
#   These values are measurement time in microseconds,
#   and inter-measurement time in milliseconds.
#   If you uncomment the line below to set a budget you
#   should use `tof.start_ranging(0)`
#   tof.set_timing(66000, 70)

    tof.start_ranging(1)  # Start ranging
                          # 0 = Unchanged
                          # 1 = Short Range
                          # 2 = Medium Range
                          # 3 = Long Range

#   Grab the range in mm, this function will block until
#   a reading is returned.
    value = tof.get_distance()

    tof.stop_ranging()
    
#    try:
#        raw_distance = value.raw_distance(sample_wait=0.3)
#    except SystemError:
#        log.log_event(
#            "error_log",
#            "ERROR - Signal not received. Possible cable or sensor problem.",
#        )
#        exit(0)

#    return round(value.depth(raw_distance, pit_depth), 1)
    return round(pit_depth - value, 1)


def water_depth():
    """Determine the depth of the water, log result and generate alert
    if needed.
    """

    critical_water_level = configs["critical_water_level"]
    water_depth = water_reading()
    if water_depth < 0.0:
        water_depth = 0.0
        log.log_reading("waterlevel", water_depth)
        log.log_event(
            "error_log",
            "ERROR - Negative reading adjusted to 0.0. Possible degrading sensor.",
        )
    log.log_reading("waterlevel", water_depth)

    if water_depth > critical_water_level and configs["alert_when"] == "high":
        alerts.determine_if_alert(water_depth)
    elif water_depth < critical_water_level and configs["alert_when"] == "low":
        alerts.determine_if_alert(water_depth)
    else:
        pass

    initiate_heartbeat()
