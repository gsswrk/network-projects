#!/usr/bin/env python3

'''
Scenario: 
Mgmt asks for a report with the latest known firmware version, device model and serial
number for all the network devices at one of your sites. Might be an audit, a report, 
or a powerpoint presentation, but they want it yesterday. This script will do just that!

Instructions: 
This script prompts for a text file consisting of a list of IP addresses (1 per line). 
Using napalm, it connects to each (CISCO IOS) device in the list to collect the hostname,
ip, model, serial number, and, os version from the running config. Once the IP list has 
been exhausted, it writes the collected data to a file named "ios_export.csv". The show-run 
parameters can be adjusted for all your reporting needs! 
'''

import napalm 
import getpass
import pandas as pd
from pandas import DataFrame

# prompts for device list. should be text file with ip per line.
device_list = open(input("Device list: "))

#credentials for connecting to network devices
user = input("Username: ")
passwd = getpass.getpass('Enter Password: ')

# opens device list and splits lines 
with device_list as f:
    lines = f.read().splitlines()

# empty lists used to store info 
hostname_list = []
ip_list = []
model_list = []
serial_numbers = []
os_version = []

# appends device info to the empty lists
def create_csv(facts, ip, hostname_list, ip_list, model_list, serial_numbers, os_version):
    hostname_list.append(facts['hostname'])
    ip_list.append(ip)
    model_list.append(facts['model'])
    serial_numbers.append(facts['serial_number'])
    os_version.append(facts['os_version'])
    print('got facts for '+ip+' with hostname: '+facts['hostname'])
    print("*************************************************")

# loops through device list, connects to each device and collects device info
# passes collected info to the create_csv function to be stored as a list
for ip in lines:
    try:
        ios_driver = napalm.get_network_driver('ios')
        ios = ios_driver(hostname=ip, username=user, password=passwd)
        ios.open()
        facts = ios.get_facts()
        create_csv(facts, ip, hostname_list, ip_list, model_list, serial_numbers, os_version)
    except Exception as e:
        print(e)
        print("*************************************************")
        continue

# creates dataframe needed for pandas
df = DataFrame({'IP': ip_list, 
                'Hostname': hostname_list, 
                'Model': model_list, 
                'Serial Number': serial_numbers, 
                'OS Version': os_version
                })

# creates local file called 'dc_ios_export.csv' 
export_csv = df.to_csv(r'ios_export.csv', index=None, header=True)

print(export_csv)
