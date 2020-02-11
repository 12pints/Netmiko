#!/usr/bin/env python
from netmiko import Netmiko
from getpass import getpass

cisco1 = {
    "host": "10.50.59.254",
    "username": "enterusername Here",
    "password": getpass(),
    "device_type": "cisco_ios",
}

net_connect = Netmiko(**cisco1)
command = "show ip int brief"

print()
print(net_connect.find_prompt())
output = net_connect.send_command(command)  #send the command, suing the netmiko simple connect, and store output to a variable called output
net_connect.disconnect()      #disconnect connection
print(output)  #print the output
print()
