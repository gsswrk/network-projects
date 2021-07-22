#!/usr/bin/env python3

#steps:
# 1 - log into ios device
# 2 - find access points using lldp
# 3 - grab mac address & port, store as var
# 4 - connect to mist api
# 5 - store all ap info as json
# 6 - grab name of AP and store as var
# 7 - update port desc with name of AP

import requests
import getpass 
import json 
import napalm
import re
import time

#api creds
email = input('Mist E-mail: ')
p=getpass.getpass('Enter Mist Password: ')


mist_raw = requests.get('https://api.mist.com/api/v1/orgs/{{ org_id }}', auth=(email, p))  
mist = mist_raw.json()

with open('idf_list_named') as idf_list:
    idf_list_named = json.loads(idf_list.read())

#blank dictionary to be used for storing interface id[key] and the name of the AP[value]
dicts = {}

#loop through all detected devices, pull mac address and 
#removes "." before passing it to the mistsearch function
def extractmaclldp(lldp, mist):
    print('cleaning mac address')
    for interface in lldp:
        for port_hostname in lldp[interface]:
            mac = port_hostname['port']
            cleanmac = re.sub('\.', '', str(mac))
            mistsearch(cleanmac, mist, interface, dicts)

#takes the AP mac and tries to find a match in the data from mist
#if match is found, store key value pair in dicts 
def mistsearch(mac, mist, interface, dicts):
    for device in mist:
        try:
            if device['mac'] == mac:
                dicts[interface] = device['name']
                print('match found, added to database')
            else:
                pass
        except Exception as e:
            print(e)
            print("*" * 50)
            continue

def mainfunct(idf_list_named, mist):
    for device_name, ip in idf_list_named.items():
        try:
            user = 'username'
            passwd = 'password'
            print("*" * 50)
            print('trying: '+device_name)
            #connect to device using napalm to get lldp neighbors 
            ios_driver = napalm.get_network_driver('ios')
            ios = ios_driver(hostname=ip, username=user, password=passwd)
            ios.open()
            lldp = ios.get_lldp_neighbors()
            #create new dictionary of interfaces and associated ap_name 
            extractmaclldp(lldp, mist)
            print('updating interface descriptions')
            #loop through new dictionary of interface:ap_name pairs
            for key in dicts:
                try:
                    print('updating interface ' + key)
                    ios.cli(["configure terminal\ninterface "+key+"\ndescription "+dicts[key]+"\nend\n"])
                    time.sleep(2)
                except Exception as e:
                    print(e)
                    print("*" * 50)
                    continue
            #save config
            print('Saving config \n')
            ios.cli(["write memory\n"])
            time.sleep(3)
            print('clearing db \n')
            ios.close()
            dicts.clear()
            print("*" * 50)
            #disconnect from ios device
        except Exception as e:
            dicts.clear()
            print(e)
            print("*" * 50)
            continue

mainfunct(idf_list_named, mist)
