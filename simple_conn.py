#!/usr/bin/env python
from netmiko import Netmiko
from getpass import getpass


#below method, connects to 10.50.59.254 with the username, log on
#prompts password connects and disconnects again

net_connect = Netmiko(
    "10.50.59.254",
    username="enterusernameHere",
    password=getpass(),
    device_type="cisco_ios",
)

print(net_connect.find_prompt())
net_connect.disconnect()
