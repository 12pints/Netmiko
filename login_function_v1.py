###Version 1.0 - 9th december 2019

from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException, NetMikoAuthenticationException
import textfsm
import datetime
import os
from getpass import getpass
import multiprocessing

def login ( host, ip, user, pw , protocol = 'both') :
    ## Define known password want to try
    username = []
    password = []
    ssh_status = ""
    telnet_status = ""
    
    ## Check the username/password that user input first
    username.insert (0,user)
    password.insert (0,pw)
    
    authenticated = False
    protocols = ['cisco_ios','cisco_ios_telnet']
    
    if protocol.upper() == "SSH"  :
        protocols = ['cisco_ios']

    if protocol.upper() == "TELNET"  :
        protocols = ['cisco_ios_telnet']
        
    for i in range(0 , len(username)):
        cisco  = {
            'device_type' : 'cisco_ios',
            'ip' : ip,
            'username' : username[i],
            'password' : password[i],
            'global_delay_factor' : 0.8 , 
        }
        
        ## Try protocol define in the protocols
        con = None
        ssh_status = "Not Try"
        telnet_status = "Not Try"
        
        for pro in protocols:
            cisco['device_type'] = pro

            error = 0
            error_msg = ""
            
            
            # print username[i]
            try:
                con = ConnectHandler(**cisco)
                error_msg = "OK"
                authenticated = True                
            except NetMikoAuthenticationException:
                error = 1
                error_msg = "Authentication error"
            except NetMikoTimeoutException:
                error = 2
                error_msg = "Timeout"
            except Exception as e:
                error = 3
                error_msg = e
            
            if error != 0:
                write_to_file("Cannot login " + host + " Error: " + str(error_msg) + "\n", r'error\login_error.txt')
            
            if pro == "cisco_ios" :
                ssh_status = error_msg
            if pro == "cisco_ios_telnet" :
                telnet_status = error_msg
                
    print (ip, authenticated, ssh_status, telnet_status)
    
    return {'connect' : con, 'authenticated' : authenticated, 'ssh': ssh_status, 'telnet':telnet_status, 'hostname' : host, 'ip': ip}
   

def regEx (regExString, stringToSearch):
    stringRegex = re.compile(regExString)
    matchObject = stringRegex.search(stringToSearch)
    
    if matchObject is not None:
        return matchObject.group(1).strip()
    else: 
        return ("NA")
   
def write_to_file(string, full_path):
    f = open (full_path,'a')
    f.write (string + "\n")
    f.close ()

#this function gets called in point #AA1 in the find_port.py script and loads the file with the switches to create list of hosts
def read_list():                                   
    f = open ("switches.txt")
    content = f.read ()
    content_lines = content.splitlines ()
    host_name = []
    # host_ip  = []
    for line in content_lines:
        if line.strip () != "" :
            info = line.split(",")
            host_name.append(info[0])
            # host_ip.append(info[1])
    # return host_name, host_ip
    return host_name

def send_command_multiprocessing (host, ip):
    failed_host_path = r'error\failed_list.txt'
    
    user = "<insert user here>"
      
    # If SSH not work
    output_ssh1 = login (host, ip, user, pw, 'ssh')
    
    # if output_ssh1['connect'] is None:
        
    # else:
        # try:
            # write_to_file (output_ssh1['connect'].send_command("show run"), 'config\\' + host + '.txt')
        # except Exception as e:
            # write_to_file (host + "," + str(output_ssh1['ssh']) + ",Able login via ssh but fail to save config\n", failed_host_path)
    
    
    # output_ssh2 = login (host, ip, user, pw, 'ssh')
    # if output_ssh2['connect'] is None:
        # write_to_file(host + "," + str(output_ssh2['ssh']) + ",Able login via Telnet not able to enable SSH" + "\n", failed_host_path)
    # else:
        # try:
            # command_disable_telnet_output =  output_ssh2['connect'].send_config_set(telnet_disable_set)
            # write_to_file (command_disable_telnet_output, 'log\\' + host + "_telnet_disable" + ".txt")
            # write_to_file (host + "\n", 'log\\' + "done_list.txt")
        # except Exception as e:
            # write_to_file (host + "," + "Able login via SSH but fail to execute telnet disable command" + "\n", failed_host_path)      
    # return 0
    
    
    

def main ():
    host_name = []
    # host_ip  = []
    
    authenticated_list = []
    ssh_status_list = []
    telnet_status_list = []
    host_name = read_list ()
    # host_name, host_ip = read_list ()
    print (host_name)
    # for i in range (0 , len(host_name)):
        # send_command_multiprocessing (host_name[i] , host_ip[i])
    # host_name, host_ip = read_list ()
    
   
    
    # host = 'fq6488ar101'
    
    # print (output['connect'].send_config_set("crypto key generate rsa modulus 1024"))
    

if __name__ == "__main__" :
    main()
