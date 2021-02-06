#!/usr/bin/env python

import subprocess
import optparse
import re

#Module to get the arguments from the CLI
def get_arguments():
    # Call the option parser module
    parser = optparse.OptionParser()
    # Add the interface option to pass interface desired to be changed
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    # Added the option new MAC
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    #Parse the arguments
    (options, arguments) = parser.parse_args()
    #if the options interface parameter does not exist return an error
    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
    #if the options parameter is not set return an error
    elif not options.new_mac:
        parser.error("[-] Please specify a new mac, use --help for more info.")
    #Return options
    return options

#Module to change tha mac address
def change_mac(interface, new_mac):
    # Print Changing mac address positive note
    print("[+] Changing MAC address for " + interface + " to " + new_mac)
    #Make sub process calls, turning the interface
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

#Module to grab the current mac address
def get_current_mac(interface):
    #get the process check out from ifconfig interface
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    # Decode the subprocess check output to utf to make sure it can be searched with regex
    ifconfig_result = ifconfig_result.decode('utf-8')
    #Use re module to perform a regex search and find the MAC address
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    #if the regex returns a result
    if mac_address_search_result:
    #return mac address
       return mac_address_search_result.group(0)
    else:
    #Else Print an Error that mac address can not be read
        print("[-] Could not read MAC address.")

# Get the command line arguments and store it in a variable
options = get_arguments()

#get the current mac by calling get current mac function
current_mac = get_current_mac(options.interface)

#Display Current Mac address
print("CURRENT MAC = " + str(current_mac))

#Change the mac address with current mac and new mac parameters
change_mac(options.interface, options.new_mac)

#Get the current MAC
current_mac = get_current_mac(options.interface)

#If the current mac is the same as the MAC entered
if current_mac == options.new_mac:
    ## Print the new mac
    print("[+] MAC address was successfuly changed to " + current_mac)
else:
    #Otherwise print an error
    print("[-] MAC address did not get changed.")






