#!/usr/bin/env python

import scapy.all as scapy


def scan(ip):
    # print('Building packet...')
    # Arp Request
    # scapy.arping(ip)
    arp_request = scapy.ARP(pdst=ip)
    # scapy.ls(arp_request)  # This will show the fields for the ARP class.
    # print(arp_request.summary())  # Show ARP Object summary
    # arp_request.show()

    # Ethernet Broadcast
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")  # Ethernet Object
    # scapy.ls(broadcast)  # This will show the fields for the Ether class.
    # print(broadcast.summary())
    # broadcast.show()

    # Arp/ Broadcast Packet  Put the MAC Broadcast and ARP together!
    arp_request_broadcast = broadcast/arp_request
    # print(arp_request_broadcast.summary())
    # arp_request_broadcast.show()
    # print('Packet complete...')

    # Sending the packet / Receive the Response
    # Capture two lists of values
    (answered_list, unanswered_list) = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)
    # print(answered_list.summary())
    results = []
    print('IP\t\t\tMAC Address\n-----------------------------------------------------')
    for element in answered_list:
        # print(element[1])  # This will show the raw packet data.
        # print(element[1].show())  # This will show the response fields.
        # print(element[1].psrc)  # Packet Source - IP
        # print(element[1].hwsrc)  # Hardware Source - MAC
        print(element[1].psrc + '\t\t' + element[1].hwsrc)
        print('-----------------------------------------------------')
        results.append((element[1].psrc, element[1].hwsrc))

    return results


results = scan("192.168.1.1/24")


# Answered Object, There's actually a tuple in here. [0] and [1] < which has the response data.
# (<Ether  dst=ff:ff:ff:ff:ff:ff type=ARP |<ARP  pdst=192.168.1.1 |>>,
# <Ether  dst=00:c0:ca:97:1a:76 src=38:94:ed:b8:f4:02 type=ARP |
# <ARP  hwtype=0x1 ptype=IPv4 hwlen=6 plen=4 op=is-at hwsrc=38:94:ed:b8:f4:02 psrc=192.168.1.1
# hwdst=00:c0:ca:97:1a:76 pdst=192.168.1.24 |>>)
