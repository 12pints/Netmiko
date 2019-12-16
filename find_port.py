#version 1_0 working 16 december 2019

from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException, NetMikoAuthenticationException
import textfsm
import datetime
import os
from getpass import getpass
import multiprocessing
###the actual login code lives in a separate py file called login_function
from login_function_v1 import *  


def show_flash_free(show_int_counter):
    lines = show_int_counter.splitlines()
    # declare empty
    free_size = []  
    for line in lines:
        if 'free' in line:
            # print (line)
            words = line.split("(")
            # print (counter)
            free_size.append(words[1])
    return free_size


def send_command_devices(host, username, password):
    failed_host_path = r'error\failed_list.txt'
    # this calls the function above, and executes show flash
    ssh_login = login(host, host, username, password, 'ssh')
    if ssh_login['connect'] is not None:
        show_flash = ssh_login["connect"].send_command(
            "show flash:")  
        print(show_flash)
        port_free = show_flash_free(show_flash)
        write_to_file("{},{}".format(host, port_free), 'output.txt')
        ssh_login['connect'].disconnect()

###### starting point of code
def main():
    # this is a reference to login_function_v1 (imported at start of this script)  and is a fucntion that loads switches.txt point #AA1
    host_names = read_list()  
    username = input("insert username here: ")
    # prompt to input password, at this point will get echoed
    password = getpass("password:")  

    # this calls the function above send_command_devices
    for host in host_names:
        send_command_devices(host, username, password)  


if __name__ == "__main__":
    main()
