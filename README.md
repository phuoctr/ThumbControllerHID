# Tutorial: Thumb-mounted controller

This thumb-mounted controller is an input device for use in extended reality (XR) environments, it operates by sensing its user’s thumb gestures in which thumb contact and movements are processed using various output data. This data is gathered from 2 or more force sensitive resistors and a gyroscope. Recognised gestures are then sent to an XR device via Bluetooth Low Energy (BLE).
In this version, the Thumb-mounted controller uses Adafruit CircuitPython libraries for creating a BLE keyboard profile

## Materials
### Seeed Xiao BLE Sense
This is a BLE development board which comes with a built-in accelerator and gyroscope. The Xiao BLE Sense can be found on the [SEEED website](https://www.seeedstudio.com/Seeed-XIAO-BLE-Sense-nRF52840-p-5253.html).

### Force-Sensitive Resistors (FSRs) 
Two 30g minimum sensitivity resistors are recommended for better gesture recognition. The FSRs can be purchased quite readily but a 0-2kg sensitive FSR on [AliExpress](https://www.aliexpress.com/item/32853977086.html?spm=a2g0o.order_detail.0.0.274ef19cbF8s2J) is a good example.

### Resistors
Two 10,000Ω resistors are required for the controller to function properly. Wattage is not a concern for this device as the board has relatively low power consumption. The resistors can be purchased online fairly easily. However, for beginners, [this guide](https://wiraelectrical.com/10k-ohm-resistor-color-code/) shows the color code for the resistors.

### Li-Po Battery
For this controller, a 3.3V 25mAH battery is soldered on the board. For a more advanced setup, the controller can also be powered by a USB-C port. Without it, however, the battery will last for ~2 hours before it needs to be replaced. So it is up to the user's discretion to decide whether to use the USB-C port or the 25mAH battery.
> Note: The power consumption is not very significant, so some battery banks will only work for a few seconds before the controller loses power.

### 3D Printed Housing
This housing should be printed with [TPU filament](https://www.amazon.com/NinjaTek-3DNF01117505-NinjaFlex-Filament-Midnight/dp/B078JGZRCK/ref=sr_1_19?crid=1TTAU3LOV2P8C&keywords=tpu+filament&qid=1657919414&sprefix=tpu%2Caps%2C93&sr=8-19) (link is an example only) for better fitting. The `.stl` file for this housing can be found [here](Housing.stl).

## Controller Architecture
FSRs play an important role on this controller for touch recognition (i.e. swiping and pressing). To use the force sensors, we need to make a voltage divider circuit as shown in the figure below. 

<figure>

<img width="845" src="https://user-images.githubusercontent.com/46408299/177761100-f0ee7b94-2d76-4f06-a61f-bbc0848b6b67.png" alt="Force-Sensitive Resistors connected to a voltage divider">

<figcaption align="center"><b>A 3V power contact is connected to one pin on each FSR while the other pin (the analog input and ground) is connected to the resistor.</b></figcaption>

</figure>

## Software Setup
To program the Adafruit Feather Sense board, a few setup steps are needed first.
1. [Set up CircuitPython on the Seeed board](https://wiki.seeedstudio.com/XIAO-BLE_CircutPython/)
2. Import `adafruit_ble` and `adafruit_lsm6ds` libraries. The documentation for these libraries can be found [here](https://docs.circuitpython.org/projects/ble/en/latest/) and [here](https://docs.circuitpython.org/projects/lsm6dsox/en/latest/api.html) respectively. The `adafruit_ble` library is used to create the BLE keyboard profile. The `adafruit_lsm6ds` library is used to create the accelerometer and gyroscope. To install the libraries, run the following command in a terminal:
```
pip3 install adafruit-circuitpython-ble adafruit-circuitpython-lsm6ds
```
> Note: A virtual environment is recommended for this setup. You can create one easily by following this [guide](https://realpython.com/python-virtual-environments-a-primer/#create-it).

## Hardware Details
The housing is comprised of two parts, one for holding the Xiao BLE Sense board and the other for mounting the user’s thumb. Under the thumb mount, the force sensitive pads of the two FSRs are stiched as illustrated in the figure below:

<figure>

<img width="1015" alt="image" src="https://user-images.githubusercontent.com/46408299/177760280-9ac10604-1062-4f7e-9aa3-c964e360e409.png">

<figcaption align="center"><b>The controller can be powered either by connecting to a computer or using an external battery. A battery wristband is designed for mounting the battery to the thumb mount.</b></figcaption>

</figure>

*See the [3D Printed Housing](#3d-printed-housing) section for more details on the housing.*

## Gestures
At the moment, this controller supports the following gestures:
- Swiping left/right
- Swiping up/down
- Quick press
- Long press

*More gestures will be added in the future.*

## Demo
A working demo for this controller can be found [here](https://soundxvision.io/lets-play-2048). In this demo, with the HID BLE profile uploaded to the board, I can use the thumb mounted controller for playing 2048.

## Contributions
This device was designed and developed by [SoundxVision](https://soundxvision.io) with this [thesis at VAMK](https://www.theseus.fi/handle/10024/744024) by [@phuoctr](https://github.com/phuoctr)  as a basis for the concept.

We would like to thank all of the contributors to this project.

<a href="https://github.com/phuoctr/ThumbControllerHID/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=phuoctr/ThumbControllerHID" />
</a>