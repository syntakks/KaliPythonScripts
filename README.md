# KaliPythonScripts
Python Scripts for Ethical Hacking.

# Setup
-I'm using Alfa RT3070 Adapter with Virtual Box. Use a Nat Network or bridged connection to run the following:\
`sudo apt-get update`\
`sudo apt-get install firmware-ralink`\
This will install the drivers you need. 
- Then shutdown the virtual box and disable the network in VB settings.
- Connect the WIFI dongle and make sure you get a connection.
- Create a USB filter from your USB device and then create another with just the vendor and product ID
  - Name: Alfa
  - Vendor ID: 148f
  - Product ID: 3070
  - Keeping this Generic seems to work better.
  - NOTE: I have it on USB 1.0. But have heard of others that needed it on 2.0 or 3.0
- Safely remove the WIFI device from the system tray. Then unplug it.
- Fire up the Virtual Box and Cheer! You should be able to connect to your network.
- You must do these steps every time you want to use the WIFI dongle. Otherwise the parent PC will\
take over the wifi connection and create a confusing mess!

# Scripts
mac_changer.py\
Usage: Change your MAC address on Kali-Linux\
Run: python mac_changer.py [-i, --interface] <interface> [-m, -mac] <MAC Address>\
Example: python mac_changer.py -i eth0 -m 00:11:22:33:44:55