# Write your code here :-)
# SPDX-FileCopyrightText: 2020 John Park for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
This example acts as a BLE HID keyboard to peer devices.
Attach five buttons with pullup resistors to Feather nRF52840
  each button will send a configurable keycode to mobile device or computer
"""

import time
import board
from analogio import AnalogIn

import board
import digitalio
import busio
from adafruit_lsm6ds.lsm6ds3trc import LSM6DS3TRC
from adafruit_lsm6ds import Rate, AccelRange, GyroRange

# LSM6DS3TRC
# On the Seeed XIAO nRF52840 Sense the LSM6DS3TR-C IMU is connected on a separate
# I2C bus and it has its own power pin that we need to enable.
imupwr = digitalio.DigitalInOut(board.IMU_PWR)
imupwr.direction = digitalio.Direction.OUTPUT
imupwr.value = True
time.sleep(0.1)

imu_i2c = busio.I2C(board.IMU_SCL, board.IMU_SDA)
sensor = LSM6DS3TRC(imu_i2c)
sensor.gyro_range = GyroRange.RANGE_2000_DPS

# BLE

import adafruit_ble
from adafruit_ble.advertising import Advertisement
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.standard.hid import HIDService
from adafruit_ble.services.standard.device_info import DeviceInfoService
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

hid = HIDService()

device_info = DeviceInfoService(
    software_revision=adafruit_ble.__version__, manufacturer="SoundxVision"
)
advertisement = ProvideServicesAdvertisement(hid)
advertisement.appearance = 961
scan_response = Advertisement()
scan_response.complete_name = "SxV HID"

ble = adafruit_ble.BLERadio()
if not ble.connected:
    #print("advertising")
    ble.start_advertising(advertisement, scan_response)
else:
    #print("already connected")
    #print(ble.connections)
    ble.connections

# keyboard service

k = Keyboard(hid.devices)
kl = KeyboardLayoutUS(k)

# Touch sensing mechanic

AIN0 = AnalogIn(board.A0)
AIN2 = AnalogIn(board.A2)

# HID HIDState
IDLING = 0
FIRST_ZONE_TOUCH = 1
FIRST_ZONE_START_PRESS = 2
FIRST_ZONE_PRESS_DOWN = 3
FIRST_ZONE_RELEASE = 4
SECOND_ZONE_TOUCH = 5
SECOND_ZONE_START_PRESS = 6
SECOND_ZONE_PRESS_DOWN = 7
SECOND_ZONE_RELEASE = 8
UP = 9
DOWN = 10
LEFT = 11
RIGHT = 12

# Force sensor ranges
NONE_CONTACT = 10
PRESS_DOWN = 500

# Duration
MIN_PRESS_DOWN_DURATION = 0.3
MAX_TOUCH_RELEASE = 0.05


# Initial HIDState of the device
HIDState = 0


pressDownTime = 0


timestampPress = 0
timestampRelease = 0
timestampSwipe = 0

# Swipe
SWIPING_UPDATE_INTERVAL = 0.350
SWIPING_ANGLE = 4
touchReleaseTime = MAX_TOUCH_RELEASE
swipeTime = SWIPING_UPDATE_INTERVAL
firstZoneLeft = False
firstZoneRight = False
secondZoneLeft = False
secondZoneRight = False

# Rotation
zAxisRotation = 0


while True:
    # Advertising
    while not ble.connected:
        pass

    # Once connected
    while ble.connected:
        fsr0 = AIN0.value / 64
        fsr1 = AIN2.value / 64
        if HIDState == IDLING:
            if fsr0 > NONE_CONTACT and fsr1 > NONE_CONTACT:
                pass
            if fsr0 > NONE_CONTACT:
                HIDState = FIRST_ZONE_TOUCH
                timestampSwipe = time.monotonic()
            if fsr1 > NONE_CONTACT:
                HIDState = SECOND_ZONE_TOUCH

        elif HIDState == FIRST_ZONE_TOUCH:
            if fsr0 <= NONE_CONTACT:
                if firstZoneLeft:
                    k.send(Keycode.LEFT_ARROW)
                    firstZoneLeft = False
                    # print("LEFT")
                    HIDState = IDLING

                elif firstZoneRight:
                    k.send(Keycode.RIGHT_ARROW)
                    # print("RIGHT")
                    firstZoneRight = False
                    HIDState = IDLING

                else:
                    HIDState = FIRST_ZONE_RELEASE
                    timestampRelease = time.monotonic()
            elif fsr0 >= PRESS_DOWN:
                HIDState = FIRST_ZONE_START_PRESS
                timestampPress = time.monotonic()
            else:
                if swipeTime >= 0:
                    zAxisRotation += (
                        sensor.gyro[2] * 57.2958 * (time.monotonic() - timestampSwipe)
                    )
                    swipeTime -= time.monotonic() - timestampSwipe
                    timestampSwipe = time.monotonic()
                    if zAxisRotation >= SWIPING_ANGLE:
                        firstZoneLeft = True
                        zAxisRotation = 0
                    elif zAxisRotation <= -SWIPING_ANGLE:
                        firstZoneRight = True
                        zAxisRotation = 0
                else:
                    swipeTime = SWIPING_UPDATE_INTERVAL
                    zAxisRotation = 0
                    firstZoneLeft = False
                    firstZoneRight = False

        elif HIDState == FIRST_ZONE_START_PRESS:
            if fsr0 >= PRESS_DOWN:
                pressDownTime += time.monotonic() - timestampPress
                timestampPress = time.monotonic()
            elif fsr0 <= PRESS_DOWN:
                HIDState = IDLING
            if pressDownTime >= MIN_PRESS_DOWN_DURATION:
                HIDState = FIRST_ZONE_PRESS_DOWN

        elif HIDState == FIRST_ZONE_PRESS_DOWN:
            # print("1st Press")
            k.send(Keycode.ENTER)
            HIDState = IDLING
            pressDownTime = 0

        elif HIDState == FIRST_ZONE_RELEASE:
            # print("1st Released! ", touchReleaseTime)
            touchReleaseTime -= time.monotonic() - timestampRelease
            timestampRelease = time.monotonic()
            if touchReleaseTime > 0:
                if fsr1 > NONE_CONTACT:
                    HIDState = UP
            else:
                HIDState = IDLING
                touchReleaseTime = MAX_TOUCH_RELEASE

        elif HIDState == SECOND_ZONE_TOUCH:
            if fsr1 <= NONE_CONTACT:
                if secondZoneLeft:
                    k.send(Keycode.LEFT_ARROW)
                    firstZoneLeft = False
                    # print("LEFT")
                    HIDState = IDLING
                elif secondZoneRight:
                    k.send(Keycode.RIGHT_ARROW)
                    # print("RIGHT")
                    firstZoneRight = False
                    HIDState = IDLING
                else:
                    HIDState = SECOND_ZONE_RELEASE
                    timestampRelease = time.monotonic()
            elif fsr1 >= PRESS_DOWN:
                HIDState = SECOND_ZONE_START_PRESS
                timestampPress = time.monotonic()
            else:
                if swipeTime >= 0:
                    zAxisRotation += (
                        sensor.gyro[2] * 57.2958 * (time.monotonic() - timestampSwipe)
                    )
                    swipeTime -= time.monotonic() - timestampSwipe
                    timestampSwipe = time.monotonic()
                    if zAxisRotation >= SWIPING_ANGLE:
                        secondZoneLeft = True
                        zAxisRotation = 0
                    elif zAxisRotation <= -SWIPING_ANGLE:
                        secondZoneRight = True
                        zAxisRotation = 0
                else:
                    swipeTime = SWIPING_UPDATE_INTERVAL
                    zAxisRotation = 0
                    secondZoneLeft = False
                    secondZoneRight = False

        elif HIDState == SECOND_ZONE_START_PRESS:
            if fsr1 >= PRESS_DOWN * 0.7:
                pressDownTime += time.monotonic() - timestampPress
                timestampPress = time.monotonic()
            elif fsr1 <= PRESS_DOWN:
                HIDState = IDLING
            if pressDownTime >= MIN_PRESS_DOWN_DURATION:
                HIDState = SECOND_ZONE_PRESS_DOWN

        elif HIDState == SECOND_ZONE_PRESS_DOWN:
            # print("2ND Press")
            k.send(Keycode.ESCAPE)
            HIDState = IDLING
            pressDownTime = 0

        elif HIDState == SECOND_ZONE_RELEASE:
            # print("2ND Released! ", touchReleaseTime)
            touchReleaseTime -= time.monotonic() - timestampRelease
            timestampRelease = time.monotonic()
            if touchReleaseTime > 0:
                if fsr0 > NONE_CONTACT:
                    HIDState = DOWN
            else:
                HIDState = IDLING
                touchReleaseTime = MAX_TOUCH_RELEASE

        elif HIDState == UP:
            pressDownTime = 0
            # print("UP")
            k.send(Keycode.UP_ARROW)
            HIDState = IDLING

        elif HIDState == DOWN:
            pressDownTime = 0
            # print("DOWN")
            k.send(Keycode.DOWN_ARROW)
            HIDState = IDLING

    ble.start_advertising(advertisement)
