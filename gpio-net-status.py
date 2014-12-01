import os, sys
import subprocess
import RPi.GPIO as GPIO
import time
import signal

GPIO.setmode( GPIO.BCM )

ledAR = 6
ledAG = 26
ledBR = 12
ledBG = 20

btnA = 18
btnB = 23

statusWifi = False
statusProxy = False



def resetWifiAction(channel):
#	print( "Resetting wifi\n" )
	clearLedStatus()
	subprocess.call( ["ifconfig","wlan0","down"] )
	time.sleep( 3 )
	subprocess.call( ["ifconfig","wlan0","up"] )
	return True;

def resetVpnAction(channel):
	print( "Resetting VPN\n" )
	clearLedStatus()
	subprocess.call( ["/etc/init.d/openvpn","stop"] )
	time.sleep(3);
	subprocess.call( ["/etc/init.d/openvpn","start"] )
	return True;

def cleanupAction( signum, frame ):
	GPIO.cleanup()
	print( "Have a good day\n" )
	sys.exit()

def checkWifiStatus():
	result = subprocess.check_output( ["ifconfig", "wlan0"] )
	if ( b"inet addr:" in result ):
		return True
	else:
		return False
	
def checkProxyStatus():
#	result = subprocess.check_output( ["curl", "-s", "ifconfig.me"] )
#	if ( b"37.48.71.70" in result ):
#		return True
#	else:
#		return False

	FNULL = open(os.devnull, 'w')
#	result = subprocess.call( ["ping", "-c", "1", "-I", "tun0", "10.9.0.1"], stdout=FNULL, stderr=subprocess.STDOUT, close_fds=True )
	result = subprocess.call( ["fping", "-r0", "-t400", "-q", "10.9.0.1"], stdout=FNULL, stderr=subprocess.STDOUT, close_fds=True )
	if result == 0:
		return True
	else:
		return False



def setLedStatus( statusWifi, statusProxy ):
	if ( statusWifi ):
		GPIO.output( ledAG, 1 )
		GPIO.output( ledAR, 0 )
	else:
		GPIO.output( ledAG, 0 )
		GPIO.output( ledAR, 1 )

	if ( statusProxy ):
		GPIO.output( ledBG, 1 )
		GPIO.output( ledBR, 0 )
	else:
		GPIO.output( ledBG, 0 )
		GPIO.output( ledBR, 1 )

def clearLedStatus():
	GPIO.output( ledAR, 1 )
	GPIO.output( ledAG, 1 )
	GPIO.output( ledBR, 1 )
	GPIO.output( ledBG, 1 )

GPIO.setup( btnA, GPIO.IN, pull_up_down=GPIO.PUD_DOWN )
GPIO.setup( btnB, GPIO.IN, pull_up_down=GPIO.PUD_DOWN )

GPIO.add_event_detect(btnA, GPIO.RISING, callback=resetWifiAction)
GPIO.add_event_detect(btnB, GPIO.RISING, callback=resetVpnAction)

GPIO.setup( ledAR, GPIO.OUT )
GPIO.setup( ledAG, GPIO.OUT )
GPIO.setup( ledBR, GPIO.OUT )
GPIO.setup( ledBG, GPIO.OUT )

signal.signal( signal.SIGINT, cleanupAction )
signal.signal( signal.SIGTERM, cleanupAction )

while True:
	clearLedStatus()
	statusWifi = checkWifiStatus()
	statusProxy = checkProxyStatus()
	setLedStatus( statusWifi, statusProxy )
	time.sleep(5)

