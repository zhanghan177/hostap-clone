# autoscan tests
# Copyright (c) 2014, Jouni Malinen <j@w1.fi>
#
# This software may be distributed under the terms of the BSD license.
# See README for more details.

import time
import logging
logger = logging.getLogger()
import os

import hostapd

def test_autoscan_periodic(dev, apdev):
    """autoscan_periodic"""
    hostapd.add_ap(apdev[0]['ifname'], { "ssid": "autoscan" })

    try:
        if "OK" not in dev[0].request("AUTOSCAN periodic:1"):
            raise Exception("Failed to set autoscan")
        dev[0].connect("not-used", key_mgmt="NONE", scan_freq="2412",
                       wait_connect=False)
        times = {}
        for i in range(0, 3):
            logger.info("Waiting for scan to start")
            start = os.times()[4]
            ev = dev[0].wait_event(["CTRL-EVENT-SCAN-STARTED"], timeout=5)
            if ev is None:
                raise Exception("did not start a scan")
            stop = os.times()[4]
            times[i] = stop - start
            logger.info("Waiting for scan to complete")
            ev = dev[0].wait_event(["CTRL-EVENT-SCAN-RESULTS"], 10)
            if ev is None:
                raise Exception("did not complete a scan")
        if times[0] > 1 or times[1] < 0.5 or times[1] > 1.5 or times[2] < 0.5 or times[2] > 1.5:
            raise Exception("Unexpected scan timing: " + str(times))
    finally:
        dev[0].request("AUTOSCAN ")

def test_autoscan_exponential(dev, apdev):
    """autoscan_exponential"""
    hostapd.add_ap(apdev[0]['ifname'], { "ssid": "autoscan" })

    try:
        if "OK" not in dev[0].request("AUTOSCAN exponential:2:10"):
            raise Exception("Failed to set autoscan")
        dev[0].connect("not-used", key_mgmt="NONE", scan_freq="2412",
                       wait_connect=False)
        times = {}
        for i in range(0, 3):
            logger.info("Waiting for scan to start")
            start = os.times()[4]
            ev = dev[0].wait_event(["CTRL-EVENT-SCAN-STARTED"], timeout=5)
            if ev is None:
                raise Exception("did not start a scan")
            stop = os.times()[4]
            times[i] = stop - start
            logger.info("Waiting for scan to complete")
            ev = dev[0].wait_event(["CTRL-EVENT-SCAN-RESULTS"], 10)
            if ev is None:
                raise Exception("did not complete a scan")
        if times[0] > 1 or times[1] < 1 or times[1] > 3 or times[2] < 3 or times[2] > 5:
            raise Exception("Unexpected scan timing: " + str(times))
    finally:
        dev[0].request("AUTOSCAN ")
