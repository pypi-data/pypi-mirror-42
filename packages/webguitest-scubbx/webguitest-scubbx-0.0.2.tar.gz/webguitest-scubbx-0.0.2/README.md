# WebGuiTest
A web user interface test module for Python 3 combining Selenium and pyautogui into one interface

## Requirements

Ideally you have both, Selenium and the pyautogui module installed. Both are freely available.
Selenium is used for base interaction with the FireFox web browser and to interact with HTML elements when they need to be selected by their ''id'', ''name'' or ''CSS path''.
Pyautogui is used when a portion of the screen needs to be identified by a screenshot. This is helpful, if you need to find a button that has a random ID.

### Selenium

Selenium is a web testing framework used to auto-perform interactions with websites by selecting elements in the DOM of the HTML. It can be used to control many different browsers. WebGuiTest is using only the FireFox browser.

You need to install the selenium driver for python

    pip install selenium

and download the so-called ''geckodriver'' for Selenium to let it interact with an existing installation of the FireFox browser. You can find the current version of the ''geckodriver'' here: https://github.com/mozilla/geckodriver/releases
You have to unpack it and copy the file to a location where your python installation can find the file (e.g. somewhere in your systems $PATH).

### pyautogui

The pyautogui library is simply installed by

    pip install pyautogui

On Linux you additionally need to install the Xlib libary with

    pip install xlib

and the scrot program for taking screenshots:

    apt install scrot

## Changelog

### 0.0.2

Added "enterValueToGraphic" function

### 0.0.1

First release
