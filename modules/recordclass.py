#!/usr/bin/python
"""
Module for defining class for record.  Gathers information either from input (passed) or
prompts for missing input.

Creates file to track activity.
"""

# Import Modules

import sys
import time
import getpass
import os

# Global Variables

# Class Definitions

class Record(object):
    def __init__(self, options):
        """
        Description: Set all local class variables to default
        
        Input: None
        Output: None
        """
        self.devices = []
        self.commands = []
        
        if options['userid'] == "":
            self.userid = raw_input('Please enter your User ID: ')
        else:
            self.userid = options['userid']
        
        if options['username'] == "":
            self.username = raw_input ('Please enter your name: ')
        else:
            self.username = options['username']
        
        if options['password'] == "":
            self.password = getpass.getpass(prompt='Please enter your Password: ')
        else:
            self.password = options['password']
        
        if options['enablepassword'] == "":
            self.enablepassword = getpass.getpass(prompt = 'Please enter the enable Password: ')
        else:
            self.enablepassword = options['enablepassword']
        
        if options['devicefile'] == "" or not os.path.isfile(options['devicefile']):
            self.devicefile = raw_input("Please enter the filename that contains the device list: ")
            self.devices = self.read_file(self.devicefile)
        else:
            self.devices = self.read_file(options['devicefile'])
        
        if options['commandfile'] == "" or not os.path.isfile(options['commandfile']):
            self.commandfile = raw_input("Please enter the filename that contains the command list: ")
            self.commands = self.read_file(self.commandfile)
        else:
            self.commands = self.read_file(options['commandfile'])
        
        if options['transport'] == "":
            self.transport = raw_input("Please enter the desired transport (ssh / telnet): ")
        else:
            self.transport = options['transport']
        
        self.parentdirect = options['parentdirect']
        if os.path.isdir(self.parentdirect):
            os.chdir(self.parentdirect)
        else:
            self.create_directory(str(self.parentdirect))
            os.chdir(self.parentdirect)
            
        if options['direct'] == "":
            print
            print "The Unique Identifier will be used to create a sub directory in the repository"
            print "and also to name files.  In most cases, something meaningful to the implelementation"
            print "such as the change control id"
            self.direct = raw_input('Please enter your Unique Identifier: ')
        else:
            self.direct = options['direct']
        
        while os.path.isdir(self.direct):
            self.direct = raw_input("Looks like that directory already exists, please enter a unique identifier: ")
        self.create_directory(str(self.direct))
            
        self.setup()
        
    def __str__(self):
        """
        Description: Provide string representation of class information
        
        Input: None
        Output: String
        """
        result = ""
        result += "UserID = " + str(self.userid) + "\n"
        result += "Password = " + str(self.password) + "\n"
        result += "Enable Password = " + str(self.enablepassword) + "\n"
        result += "Device File = " + str(self.devicefile) + "\n"
        result += "Command File = " + str(self.commandfile) + "\n"
        result += "Parent Directory = " + str(self.parentdirect) + "\n"
        result += "Sub Directory = " + str(self.direct) + "\n"
        
        return result
             
    def yesorno(self, input):
        """
        Description: Helper function to determine users intent
        
        Input: user input
        Output: Boolean
        """
        
        if input == "y" or input == "Y" or input == "yes" or input == "Yes" or input == "YES":
            result = True
        elif input == "n" or input == "N" or input == "no" or input == "No" or input == "NO":
            result = False
        else:
            input = raw_input('Incorrect input, please try again (y / n) : ')
            result = self.yesorno(input)
        
        return result
        
    def create_directory(self, directory):
        """
        Description: Prompts user for information and creates a file (and directory if 
        necessary)
        
        Input: None
        Output: None
        """
        
        while not directory.isalnum():
            print "Directory must be Alpha Numeric Only, with no Spaces."
            directory = raw_input("Please enter a valid directory name: ")
            self.direct = directory 
        
        # First check to see if the directory exists...  if not, make one.
        if not os.path.exists(directory):
            os.makedirs(directory)
            print "created " + directory
            
    def setup(self):
        """
        Description: Write initial Readme file with details
        
        Input: None
        Output: None
        """
                
        filetime = time.strftime("%d_%m_%Y_%H-%M-%S")
        file = open(self.direct + "/" + 'README', 'w')
        file.write("================================================" + "\n")
        file.write("Created by: " + self.username + " (" + self.userid + ")\n")
        file.write("Created on: " + filetime + "\n")
        file.write("Unique ID: " + self.direct + "\n")
        file.write("================================================")
        file.write("\n")
        
        file.write("========Devices Affected========\n")
        for device in self.devices:
            file.write(device + "\n")
        file.write("\n")
        
        file.write("========Commands========\n")
        for command in self.commands:
            file.write(command + "\n")
            
        file.close()
    
    def writeoutput(self, device, command, output):
        """
        Description: Takes string and writes it to a file.
        
        Input: Device Name and Output from Device
        Output: None
        """
        if self.direct not in os.getcwd():
            os.chdir(self.direct)

        filetime = time.strftime("%d_%m_%Y_%H-%M-%S")
        
        print 'Creating ' + device + '_' + command + '_' + filetime + ' file'
        print '================================================================='
        print output
        
        command = command.replace(' ','_') 
        file = open(device + '_' + command + '_' + filetime, 'w')
        file.write("================================================" + "\n")
        file.write("Created by: " + self.username + " (" + self.userid + ")\n")
        file.write("Created on: " + filetime + "\n")
        file.write("Unique ID: " + self.direct + "\n")
        file.write("================================================")
        file.write("\n")
        
        file.write("========Output========\n")
        file.write(output)
        
        file.close()
    
    def createcomponent(self):
        """
        Description: Takes relevant fields and populates a dictionary to be used to login
        
        Input: None
        Output: Dictionary
        """
        result = {}
        
        result['userid'] = self.userid
        result['password'] = self.password
        result['enablepassword'] = self.enablepassword
        result['transport'] = self.transport
        
        return result
        
    def getpass(self):
        """
        Description: Return Password as String
        
        Input: None
        Output: String
        """
        return self.password
        
    def getenable(self):
        """
        Description: Return Enable Password
        
        Input: None
        Output: String
        """
        return self.enablepassword
        
    def getdevices(self):
        """
        Description: Return List of Devices
        
        Input: None
        Output: String
        """
        return self.devices
        
    def getcommands(self):
        """
        Description: Return List of Commands
        
        Input: None
        Output: String
        """
        return self.commands
        
    def read_file(self, input):
        """
        Description: Read device file and populate list with file names
        
        Input: Filename
        Output: List
        """
        
        while not os.path.isfile(input):
            input = raw_input('Please enter filename :')

        file = open(input)        
        results = file.readlines()
        results = [line.rstrip('\n') for line in results]
        
        return results

