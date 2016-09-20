#!/usr/bin/python
"""
Module for defining class for network component.  Handles login (either Telnet or SSH, 
setting term length, entering commands (including validation of success), and closing session. 
"""

import re
import pexpect

class NetworkComponent(object):
    """
    Defines an object and performs tasks on that object
    """
    def __init__(self, device, input):
        """
        Assign variables within class
        """
        self.user = input['userid']
        self.password = input['password']
        self.enpassword = input['enablepassword']
        self.transport = input['transport']
        self.os = ""
        if self.transport == "telnet":
            self.session = pexpect.spawn('telnet ' +device)
        elif self.transport == "ssh":
            self.session = pexpect.spawn('ssh ' +self.user+'@'+device)

        
    def __str__(self):
        """
        Return information regarding the object
        """
        result = "\n++++++++++Information++++++++++++\n"
        result += "User: " + str(self.user) + "\n"
        result += "Password: " + str(self.password) + "\n"
        result += "Enable Password: " + str(self.enpassword) + "\n"
        result += "OS: " + str(self.os) + "\n"
        result += "Transport: " + str(self.transport) + "\n"
        result += "++++++++++++++++++++++++++++++++++"
        
        return result
        
    def login(self):
        """
        Input : None
        Output: None
        """
        
        response = self.session.expect(['[Uu]sername', '[Ll]ogin:', '[Pp]assword:', 'to continue connecting (yes/no)?'])
        print response
        if response == 0 or response == 1:
            self.session.sendline(self.user)
            self.session.expect('[Pp]assword:')
            self.session.sendline(self.password)
        elif response == 2:
            self.session.expect('[Pp]assword:')
            self.session.sendline(self.password)
        elif response == 3:
            self.session.sendline('yes')
            self.session.expect('[Pp]assword:')
            self.session.sendline(self.password)
            
        # Determine whether current session is enabled
        response = self.session.expect(['#', '>'])
        
        if response == 1:
            # Device is not enabled so we enable it
            self.session.expect('[Pp]assword:')
            self.session.sendline(ENABLE_PASSWORD)
            self.session.expect('#')
        
        print "=> Completed Login and Enabled Sucessfully"

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
    
    def getosfamily(self):
        """
        Description: Determine IOS Family (NXOS, IOS XR, IOS XE, IOS)
        
        Input: None
        Output: String indicating OS
        """
        input = self.sendcommand('show version')
        
        patterns = ['IOS XR', 'IOS-XE', 'NX-OS']
        result = 'IOS'
        
        for pattern in patterns:
            match = re.search(pattern, input)
            if match:
                result = pattern
                
        return result
            
    def gethwfamily(self):
        """
        Description: Determine HW Family

        Input: None
        Output: String indicating HW Type
        """

        input = self.sendcommand('show version').split("\n")
        router = None

        for line in input:

            match = re.search(r"^cisco(\s.*?\s)" ,line, re.IGNORECASE)
            if match:
                router = match.group(1)
                if "IOS" in router or "Internetwork" in router or "IOS-XE" in router:
                    router = None

            if router and match:
                return router 

    def settermlen(self):
        """
        Description: Set Term Length to 0
        
        Input: None
        Output None
        """
        
        self.session.sendline('term len 0')
        self.session.expect('#')

    def sendcommand(self, command):
        """
        Description: Send command to device
        
        Input: Command string
        Output: Return Result
        """
        self.session.sendline(command)
        self.session.expect('#')
        """
        output = self.session.expect(['#', '%'])
        
        if output == 0:
            pass
        elif output == 1:
            print "##############################################################################"
            print "Command \'" + command + "\' was not accepted"
            print
            if not self.yesorno(raw_input("Would you like to continue? (y/n)")):
                sys.exit(1)
            print "##############################################################################"
        """
        result = self.session.before

        if "% Invalid input detected" in result:
            print "Command \'" + command + "\' not accepted"
            if not self.yesorno(raw_input("Would you like to continue with the rest of the commands? (y/n) ")):
                sys.exit(1)

        return result
        
    def close(self):
        """
        Description: Close open session
        
        Input: None
        Output: None
        """
        self.session.close()


