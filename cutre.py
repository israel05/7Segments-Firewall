#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017-18 Richard Hull and contributors
# See LICENSE.rst for details.

"""
Example for seven segment displays.
"""

import time
from datetime import datetime

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.virtual import viewport, sevensegment


def date(seg):
    """
    Display current date on device.
    """
    now = datetime.now()
    seg.text = now.strftime("%y-%m-%d")


def clock(seg, seconds):
    """
    Display current time on device.
    """
    interval = 0.5
    for i in range(int(seconds / interval)):
        now = datetime.now()
        seg.text = now.strftime("%H-%M-%S")

        # calculate blinking dot
        if i % 2 == 0:
            seg.text = now.strftime("%H-%M-%S")
        else:
            seg.text = now.strftime("%H %M %S")

        time.sleep(interval)


def show_message_vp(device, msg, delay=0.5):
    # Implemented with virtual viewport
    width = device.width
    padding = " " * width
    msg = padding + msg + padding
    n = len(msg)

    virtual = viewport(device, width=n, height=8)
    sevensegment(virtual).text = msg
    for i in reversed(list(range(n - width))):
        virtual.set_position((i, 0))
        time.sleep(delay)


def show_message_alt(seg, msg, delay=0.1):
    # Does same as above but does string slicing itself
    width = seg.device.width
    padding = " " * width
    msg = padding + msg + padding

    for i in range(len(msg)):
        seg.text = msg[i:i + width]
        time.sleep(delay)


def main():
    # create seven segment device
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=1)
    seg = sevensegment(device)

    # Scrolling Alphabet Text
    print('Scrolling alphabet text...')

    filepath = 'lista.txt'
    with open(filepath) as fp:
       line = fp.readline()
       cnt = 1
       while line:
          print("Line {}: {}".format(cnt, line.strip()))
          line = fp.readline()
          if "perro" in line:
             show_message_vp(device, line)
          cnt += 1






if __name__ == '__main__':
    main()
