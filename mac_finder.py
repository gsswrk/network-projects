#!/usr/bin/env python

#import the ConnectHandler, getpass and time modules
from netmiko import ConnectHandler
import getpass
import time

#prompt for ip address
address = input('Enter Device Address: ')

#prompt for username
username = input('Enter Username: ')

#prompt for password
p=getpass.getpass('Enter Password: ')

#prompt for text file
doc = input('Enter File Name: ')

#define device dictionary
cisco_switch = {
    'device_type': 'cisco_ios',
    'ip': address,
    'username': username,
    'password': p,
}

#start ssh session
net_connect = ConnectHandler(**cisco_switch)

#opens file txt file and splits lines into list of strings 
with open(doc) as f:
    lines = f.read().splitlines()

#iterates through text file, waits 2seconds after each line
#passes mac address to device to print what interface it is connected to
for line in lines:
    result = net_connect.send_command("sh mac address-table | include " +line)
    print(result)
    time.sleep(2)

#disconnects ssh session
net_connect.disconnect()