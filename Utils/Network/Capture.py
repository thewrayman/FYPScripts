__author__ = 'Emmet'
# from scapy.all import *
#
# def pkt_callback(pkt):
#     pkt.show() # debug statement
#
# sniff(iface="eth0", prn=pkt_callback, filter="tcp", store=0)
import pcapy
import socket
import sys
import datetime
from struct import *

def main(argv):
    devices = pcapy.findalldevs()
    for d in devices:
        print "[+]Device:", d

    dev = raw_input()
    dev = devices[dev]
    print "[+]Sniffing on %s" % str(dev)

    cap = pcapy.open_live(dev, 65536, 1, 0)

