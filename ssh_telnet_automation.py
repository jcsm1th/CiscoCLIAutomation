#!/usr/bin/python
"""
This is a python script that will telnet or ssh to a list of devices and run
a list of commands on each.

Usage: ./ssh_telnet_automation.py -t telnet -o NXOS -u jasons2 -d device-list.txt -c command-list.txt

USING THE SCRIPT:
From the CLI the username, device list, command list, transport, and OS is provided.  
The script then prompts for user password and enable password.  Output is 
provided back to the console.

FORMAT OF FILES:
Both the device list and command list are text files.  Each element should
be entered one at a time as shown below.  The name of the files does not
matter as the script expects those to be provided.

example_file.txt
================
some command
some other command
yet another command

Copyright: Cisco Systems, Inc.
Created by: Jason Smith 704 339 3359
Created on: September 29, 2014
Last Update: October 8, 2014
Version: 1.0
"""
########### IMPORT MODULES #####################################################

import sys
import getopt
from modules.networkcomponent import NetworkComponent
from modules.recordclass import Record

########### GLOBAL VARIABLES ###################################################

########### CLASSES ############################################################

########### HELPER FUNCTIONS ###################################################

def usage():
    """
    Description: Provide command usage information back to user if error detected
    
    Input: None
    Output: None
    """
    print "\n=========Input Parameters==========\n"
    print "-h : help"
    print "-u <userid> : Userid"
    print "-n <username> : User Name - use \' \'"
    print "-p <password> : Password - use \' \'"
    print "-e <enable password> : Enable Password - use \' \'"
    print "-d <text file> : Device List" 
    print "-t <ssh/telnet> : Transport"
    print "-c <text file> : Command List"
    print "-r <Repository> : Repository Directory"
    print "-s <sub directory> : Sub Directory"
    print
    print "Usage: ssh_telnet_automation.py -t telnet -u jasons2 -d device-list.txt -c command-list.txt\n"
    return

def validate_input():
    """
    Description: Evaluates input and validates it conforms to what is expected
    
    Input: None
    Output: None
    """
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h1:u:n:p:e:d:t:c:r:s:")
        return opts
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)

def process_input(options):
    """
    Description: Assign global variables from arguments provided on command line.
    
    Input: Options from command input (ARGSV)
    Output: None
    """
    global DEVICELIST, COMMANDLIST
    
    result = {'userid':'', 'username':'', 'password':'', 'enablepassword':'', 'devicefile':'', 
            'transport':'telnet', 'commandfile':'', 'direct':'', 'parentdirect':'repository'}
    
    for opt, arg in options:
        if opt == "-h":
            usage()
            sys.exit()
        elif opt == "-u":
            result['userid'] = arg
        elif opt == "-n":
            result['username'] = arg
        elif opt == "-p":
            result['password'] = arg
        elif opt == "-e":
            result['enablepassword'] = arg
        elif opt == "-d":
            result['devicefile'] = arg
        elif opt == "-t":
            result['transport'] = arg
        elif opt == "-c":
            result['commandfile'] = arg
        elif opt == "-r":
            result['parentdirect'] = arg
        elif opt == "-s":
            result['direct'] = arg
        else:
            assert False, "unhandled option"
    
    return result

########### MAIN FUNCTION ######################################################

def main():
    """
    Description: This function gathers arguments from the command line and places them in
    a dictionary.  Two files are read to determine devices and commands.  Lastly, each
    device creates an object to carry out the tasks.
    """
    
    Session = Record(process_input(validate_input()))
    
    for device in Session.getdevices():
        component = NetworkComponent(device, Session.createcomponent())
        component.login()
        component.settermlen()

        for command in Session.getcommands():
            output = component.sendcommand(command)
            Session.writeoutput(device, command, output)
              
        component.close()

########### MAIN PROGRAM #######################################################

if __name__ == '__main__':
    sys.exit(main())

"""
People think that computer science is the art of geniuses but the actual reality is the 
opposite, just many people doing things that build on eachother, like a wall of 
mini stones.
- Donald Knuth
"""


