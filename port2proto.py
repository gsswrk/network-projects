#!/usr/bin/env python3

# Example program for getting service names from port number using getservbyport()of Python's scoket module

import socket
import argparse

parser = argparse.ArgumentParser(description="Look up network protocol by port number. Data comes from your local /etc/services file.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("portNumber", type=int, help="Port Number")
args = parser.parse_args()
pNumber = args.portNumber

for proto in ["tcp", "udp"]:
  try:
    serviceName = socket.getservbyport(pNumber, proto)
    if "not found" in str(serviceName):
      continue
    print(f"Name of the service running at port number {pNumber}: {serviceName} (" + proto + ")")
  except Exception as e:
    continue
