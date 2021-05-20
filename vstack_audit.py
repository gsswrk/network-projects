#!/usr/bin/env python3

import napalm
import pprint as pp
import re
from pandas import DataFrame
import getpass

# host file should just be a text document with 1 IP address per line (for now - fix inv.02 )
with open('ALL_hosts.txt', 'r') as f:
    lines = f.read().splitlines()
# device_list = input("Device File: ")

user = input("Username: ")
passwd = getpass.getpass('Enter Password: ')

# blank slate
hostname_list = []
ip_list = []
model_list = []
serial_numbers = []
statuses = []

# appends the existing lists with new host's value's 
def create_csv(facts, line, hostname_list, ip_list, model_list, serial_numbers, statuses, status):
    hostname_list.append(facts['hostname'])
    ip_list.append(line)
    model_list.append(facts['model'])
    serial_numbers.append(facts['serial_number'])
    statuses.append(status)

# determine if vstack is enable or disabled
def match_status(vstack):
    for each in vstack.splitlines():
        try:
            if re.search('enabled', each):
                pp.pprint(each)
                return each
            elif re.search('disabled', each):
                pp.pprint(each)
                return each
            elif re.search('Invalid input', each):
                pp.pprint('vstack command not recognized')
                return 'vstack command not recognized'
            else:
                pp.pprint('error or command not recognized')
                return 'error or command not recognized'
        except Exception as e:
            pp.pprint('error at match_status()')
            return 'error at match_status()'

# run through list of hosts
def lookup_main(lines, hostname_list, ip_list, model_list, serial_numbers, statuses):
    for line in lines:
        try:
            pp.pprint('***** Connecting ***** ')
            ios_driver = napalm.get_network_driver('ios')
            ios = ios_driver(hostname=line, username='x', password='x')
            ios.open()

            pp.pprint('Gathering Facts ...')
            facts = ios.get_facts()

            pp.pprint('Checking vstack config for ' + facts['hostname'] + '... ')
            vstack_out = ios.cli(['show vstack config'])
                    
            results=match_status(vstack_out['show vstack config'])

            create_csv(facts, line, hostname_list, ip_list,
                    model_list, serial_numbers, statuses, results)

            pp.pprint('***** Disconnecting ***** ')
            ios.close()
            pp.pprint('*' * 46)
        except Exception as e:
            if re.search('Authentication to device failed', str(e)):
                hostname_list.append('-')
                ip_list.append(line)
                model_list.append('-')
                serial_numbers.append('-')
                statuses.append('Authentication failed')
                pp.pprint('Authentication failed')
                continue
            else:
                hostname_list.append('-')
                ip_list.append(line)
                model_list.append('-')
                serial_numbers.append('-')
                statuses.append(str(e))
                pp.pprint(e)
                continue

lookup_main(lines, hostname_list, ip_list, model_list, serial_numbers, statuses)

# create dataframe needed for pandas
df = DataFrame({'IP': ip_list,
                'Hostname': hostname_list,
                'Model': model_list,
                'Serial Number': serial_numbers,
                'VStack Status': statuses
                })

# create local file and write to it
export_csv = df.to_csv(r'vstack_test1.csv', index=None, header=True)

pp.pprint('COMPLETE')
