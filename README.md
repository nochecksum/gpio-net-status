gpio-net-status
===============

I have a strange network setup. My cellphone provides a wifi hotspot from which I tether, my Raspberry Pi bridges that hotspot with the WLAN port of a wireless router, and the rest of my network sits on that. The RPi runs OpenVPN and all traffic is routed through that. The RPi runs headless so I needed an interface to debug and fix inevitable problems.

This script provides red/green status LEDs for a wlan0 connection and an IP address ping, and buttons to restart the wlan0 interface and restart the OpenVPN daemon.

You could of course modify it to perform all sorts of actions!

Python3 is required
fping is required (for faster pings): `sudo apt-get install fping`

Written for the extended GPIO port on the RPi B+ board, tweak accordingly for other versions. Note the `GPIO.BCM` option is set (use board pins).

Default pins are as follows:
* wlan0 success (green) output pin26
* wlan0 failure (red) output pin6
* ping success (green) output pin20
* ping success (red) output pin12
* wlan reset button input pin18
* openvpn reset button input pin23

I installed the script in my `/etc/rc.local` file (because GPIO, `openvpn` and `ifconfig up|down` require root privileges) by adding the following line:

`(sleep 10;/usr/bin/python3 /root/gpio-net-status.py)&`
