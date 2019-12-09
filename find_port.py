#Version 1.0 - 9th december 2019
#this code logs onto devices defined in switches.txt and pull the free flash (issue show flash command) output
# and puts the output into output.txt
#script relies on login_function_v1.py to be available as well, which contains the netmiko ssh login part

from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException, NetMikoAuthenticationException
import textfsm
import datetime
import os
from getpass import getpass
import multiprocessing
from login_function_v1 import *             #the actual login code lives in a separate py file


def show_flash_free (show_int_counter):

    lines = show_int_counter.splitlines()
    free_size = []                           #declare empty
    for line in lines:
        if 'free' in line:
            # print (line)
            words = line.split("(")
            # print (counter)
            free_size.append(words[1])
    return free_size


def send_command_devices (host, username, password):
    
    failed_host_path = r'error\failed_list.txt'
    
    ssh_login = login (host, host, username, password, 'ssh')
    if ssh_login['connect'] is not None:
        show_flash = ssh_login["connect"].send_command ("show flash:")    #this calls the function above, and executes show flash
        print (show_flash)
        port_free = show_flash_free (show_flash)
        write_to_file("{},{}" .format (host, port_free),'output.txt')
        ssh_login['connect'].disconnect ()

def main ():                         #starting point of code
    host_names = read_list ()        #this is a reference to login_function_v1 (imported at start of this script)  and is a fucntion that loads switches.txt point #AA1
    username  = "<insert username here>"      
    password = getpass ("password:") #prompt to input password
    
    for host in host_names:
        send_command_devices (host, username, password)     #this calls the function above send_command_devices
   
if __name__ == "__main__" :
    main()
