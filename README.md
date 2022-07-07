# Tutorial: Thumb-mounted controller

This thumb-mounted controller is an input device for using in extended reality (XR) environments, it operates by sensing user’s thumb gestures in which thumb contact and movements are processed using the output data from 2 or more force sensitive resistors and a gyroscope, recognised gestures are send to a XR device via Bluetooth Low Energy.
In this version, the Thumb-mounted controller uses Adafruit CircuitPython libraries for creating a BLE keyboard profile

## Materials

- Seeed Xiao BLE Sense: this is a bluetooth low energy (BLE) development board which comes with built-in accelerator, gyroscope. The Xiao BLE Sense can be found at [SEEED website](https://www.seeedstudio.com/Seeed-XIAO-BLE-Sense-nRF52840-p-5253.html)

- 2*Force sensitive resistors: resistors with minimum sensitve of 30gr is recommend for better gesture sensing. The force sensistive resistors can be purchased for example [A 0-2kg sensitive FSR on Aliexpress](https://www.aliexpress.com/item/32853977086.html?spm=a2g0o.order_detail.0.0.274ef19cbF8s2J).

- 2* 10,000Ohms resistors. The resistors can be bought easily from the internet.
- 3.3V Li-Po battery. For this controller, a 25mAH battery is soldered on the board but it can also be powered by the USB-C port but keep it in mind that because the power consumption is not very significant so some battery banks will only work for few second before it stop powering the controller.
- A housing for the components: this housing should be printed with TPU filament for better fitting. The stl file for this housing can be found in this repo.


## Force Sensitive Resistors

Force sensitive resistors play an important role on this controller for touch recognition including swiping and pressing. To use the force sensors, we need to make a voltage divider circuit as the figure below, a 3V power is connect to one pin on each force sensor, and on the other pin the analog input and ground is connected.

<img width="845" alt="image" src="https://user-images.githubusercontent.com/46408299/177761100-f0ee7b94-2d76-4f06-a61f-bbc0848b6b67.png">

## The program

To program the Adafruit Feather Sense board, you need to [set-up CircuitPython on the Seeed board here](https://wiki.seeedstudio.com/XIAO-BLE_CircutPython/) and use MuEditor with adafruit_ble, adafruit_lsm6ds libraries imported, the documents for these libraries can be found [lsm6dsox](https://docs.circuitpython.org/projects/lsm6dsox/en/latest/api.html) and [adafruit_ble](https://docs.circuitpython.org/projects/ble/en/latest/). 

The housing comprises of two parts, one for holding the Xiao BLE Sense board and the other for mounting user’s thumb, under the thumb mount, the force sensitive parts of two force sensitive resistors are stiched as illustrated in the figure below:

<img width="1015" alt="image" src="https://user-images.githubusercontent.com/46408299/177760280-9ac10604-1062-4f7e-9aa3-c964e360e409.png">


The controller can be powered either by connecting to a computer or using an external battery, a battery wristband is designed for mounting the battery.


## Gestures
At the moment, this controller supports following gestures, in future version of the hardware and software I hope to include more gestures
- Swiping left/right on a touch zone
- Swiping up/down
- Quick press
- Long press

A working demo for this controller can be found [here](https://soundxvision.io/lets-play-2048), in this demo, with the HID BLE profile uploaded to the board, I can use the thumb mounted controller for playing 2048.
