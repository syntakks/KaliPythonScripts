#!/usr/bin/env python

import optparse
import re
import subprocess

"""
Usage: 
    Change your MAC address on Kali-Linux
Run:
    python mac_changer.py [-i, --interface] <interface> [-m, -mac] <MAC Address>
Example:
    python mac_changer.py -i eth0 -m 00:11:22:33:44:55
"""


def get_arguments():
    max_mac_length = 17
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface for MAC address change.")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address to update interface with.")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
    elif not options.new_mac:
        parser.error("[-] Please specify a MAC, use --help for more info.")
    template = "00:00:00:00:00:00"
    options.new_mac = options.new_mac + template[len(options.new_mac):]
    if len(options.new_mac) > max_mac_length or not find_mac_in(options.new_mac):
        parser.error("[-] Invalid MAC Please specify a valid MAC Address")
    return options


def change_mac(interface, new_mac):
    previous_mac = get_current_mac(interface)
    print("[+] Current MAC Address      " + interface + ": " + str(previous_mac))
    print("[+] Changing MAC Address     " + interface + ": " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])
    current_mac = get_current_mac(interface)
    verify_mac(interface, new_mac, current_mac)


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address = find_mac_in(ifconfig_result)
    if mac_address:
        return mac_address.group(0)
    else:
        print("[-] Could not read MAC address...")


def find_mac_in(string):
    return re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", string)


def verify_mac(interface, requested_mac, current_mac):
    if requested_mac == current_mac:
        print("[+] MAC Change Success!      " + interface + ": " + str(current_mac))
    else:
        print("[-] MAC Change Failure!      " + interface + ": " + str(current_mac))


options = get_arguments()
change_mac(options.interface, options.new_mac)
