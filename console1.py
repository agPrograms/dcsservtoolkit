# Fixed a bug where server up message didnt send after a server restart.
# Fixed a bug where the server did not send a toolup message at program start.
# Fixed a bug where webhook_url was returning None, and triggering a valid condition.
# Fixed a bug where server_path was returning None, and triggering a valid condition.
# Fixed a bug where subproccess.call was not continuing with the program after the server was started in servstart(). replaced .call with .Popen.
# Added OK message for server_path check
# Added FAIL on process not running in safeexit()
# Moved toolUP rpost to servinst(), did not need a try and except when its an if condition. was not being executed.
# Removed multiple try and except conditions as they were not needed.
# Cleaned up safeexit() process and moved rpost to disc class


import subprocess
import colorama
import os
from datetime import datetime
from dotenv import load_dotenv
import time as t
import requests as r
import atexit as e

colorama.init(wrap=True)
load_dotenv('.env')

global useDiscord
global webhook_url
global dcs
webhook_url: str = os.getenv('WEBHOOK_URL')
server_path: str = os.getenv('SERVER_PATH')
useDiscord: bool = False # thinking of moving this to the .env
dcs = 'DCS_server.exe'
getTime = datetime.now()

class c:
    bl = '\033[94m'
    cy = '\033[96m'
    gn = '\033[92m'
    ok = '\033[92m'+'[OK] '
    inf = '\033[96m'+'[INFO] '
    warn = '\033[93m'+'[WARN] '
    fail = '\033[91m'+'[FAIL] '
    end = '\033[0m'\

class syS:
    # To be added later when stable code is in. Current errors will notify if the process is not able.
    #def updateNot():
        #print(f"{c.warn}Server is being updated!{c.end}")
        #return
    
    #def updateNOGO():
        #print(f"{c.fail}Can't update DCS Server if the Server Path is 'None'!{c.end}")
        #return

    def safeexit():
        if det.procfind(dcs)==False or '': # This might be a good idea, but for now. No.
            print(f"{c.fail}!***PROGRAM IS TERMINATING WITH SERVER PROCESS DEAD***!{c.end}")
            if useDiscord:disc.sendToolDOWN()
        else:
            print(f"{c.warn}!***PROGRAM IS TERMINATING***!{c.end}")
            if useDiscord:disc.sendToolDOWN()
        t.sleep(3);return 0

class det:
    def servinst(): # First call to grab/check the server process. If its not already running, we try to execute it.
        print(f"{c.ok}Started at {getTime:%H:%M:%S}{c.end}")
        print(f"{c.inf}Looking for DCS Server..{c.end}")
        if useDiscord:disc.sendToolUP # moved here from try and except at lamda, doesnt need a try and except loop cause its an if condition.
        if det.procfind(dcs) == True:
            print(f"{c.ok}DCS Server is running!{c.end}")
            if useDiscord:disc.sendServUP() # try and exceptions were not working here.
            det.servmon()
        else:
            print(f"{c.warn}DCS Server is not running.{c.end}")
            try:
                if useDiscord:disc.sendServInit()
            except:
                print(f"{c.warn}The 'WEBHOOK_URL' set in '.env' is not valid! Failed to send message to discord! Continuing...{c.end}")
            det.servstart()

    def procfind(serv_name): # Grab the process from the machine tasklist. Will return the value of the process as a string.
        call = 'TASKLIST', '/FI', 'imagename eq %s' % serv_name
        output = subprocess.check_output(call).decode()
        last_line = output.strip().split('\r\n')[-1]
        return last_line.lower().startswith(serv_name.lower())
    
    def servstart(): # Start the server from the order of another function. Catch errors if they pop up.
        print(f"{c.inf}Starting DCS Server...{c.end}")
        try:
            subprocess.Popen([str(server_path)+'\\'+dcs])
            t.sleep(30) # moved sleep from outside of try.
        except:
            print(f"{c.fail}Could not start {dcs} Please make sure 'SERVER_PATH' is set correctly in '.env'!{c.end}")
            print(f"{c.fail}Current Path: '{server_path}'{c.end}")
            if useDiscord:disc.sendCNS()
            t.sleep(10);return 0
        if useDiscord:disc.sendServUP() # removed try and except.
        det.servmon()

    def servmon(): # Monitor the process of the server executable. Check every 60 seconds.
        if det.procfind(dcs)==False or '':
            print(f"{c.warn}DCS Server is down. Restarting in 3 seconds...{c.end}")
            t.sleep(3);det.servstart()
        else:
            t.sleep(60)
            det.servmon() # theres totally a cleaner way to do this. Bad practice, I know.

class disc:
    # I can probably get rid of these functions and just send a message based on a matched dict. Like arg 'CNS' matches with the current content.
    def sendCNS():
        global dataUP
        dataUP = {
            "content": "🤕 Couldnt start the DCS Server! Something is wrong with the specified path on the box... 🆘"
        }
        try:
            r.post(webhook_url, json=dataUP)
        except:
            print(f"{c.warn}The 'WEBHOOK_URL' set in '.env' is not valid! Failed to send message to discord! Continuing...{c.end}")

    def sendServInit():
        global dataUP
        dataUP = {
            "content": "😐 DCS Server is currently down. Starting it!"
        }
        try:
            r.post(webhook_url, json=dataUP)
        except:
            print(f"{c.warn}The 'WEBHOOK_URL' set in '.env' is not valid! Failed to send message to discord! Continuing...{c.end}")

    def sendServDOWN():
        global dataUP
        dataUP = {
            "content": "⚠️ The DCS Server is down! DCS Server Toolkit is restarting it. ⚠️"
        }
        try:
            r.post(webhook_url, json=dataUP)
        except:
            print(f"{c.warn}The 'WEBHOOK_URL' set in '.env' is not valid! Failed to send message to discord! Continuing...{c.end}")

    def sendServUP():
        global dataUP
        dataUP = {
            "content": "The DCS Server is up! 👅"
        }
        try:
            r.post(webhook_url, json=dataUP)
        except:
            print(f"{c.warn}The 'WEBHOOK_URL' set in '.env' is not valid! Failed to send message to discord! Continuing...{c.end}")

    def sendToolUP():
        global dataUP
        dataUP = {
            "content": "DCS Server Toolkit is **Operational** and running **Version v2.0.0**.. Getting your server started! 😍"
        }
        try:
            r.post(webhook_url, json=dataUP)
        except:
            print(f"{c.warn}The 'WEBHOOK_URL' set in '.env' is not valid! Failed to send message to discord! Continuing...{c.end}")
    
    def sendToolDOWN():
        global dataUP
        dataUP = {
            "content": "😴 DCS Server Toolkit is exiting. Your server may also be going down too! ⚠️"
        }
        try:
            r.post(webhook_url, json=dataUP)
        except:
            print(f"{c.warn}The 'WEBHOOK_URL' set in '.env' is not valid! Failed to send message to discord! Continuing...{c.end}")

    def getHook():
        global useDiscord
        try:
            if webhook_url==' 'or 'None':
                print(f"{c.warn}Invalid or no webhook defined in '.env'!{c.end}")
                useDiscord = False # This might not be needed here. Need to do more testing.
                return False
            else:
                print(f"{c.ok}Discord Webhook set to: {webhook_url}{c.end}")
                useDiscord = True
                return True
        except:
            print(f"{c.warn}Couldn't locate 'WEBHOOK_URL' in the '.env'! You will not be able to send status messages to a discord channel!{c.end}")
            useDiscord = False
            return False
# Prints log window and banner. Make it pretty cause why not. Using lambda cause calling a function within a class is dumb for this.
@lambda _: _()
def func() -> str:
    print(f"{c.bl}**************************************{c.end}")
    print(f"{c.cy}     DCS Server Essentials Toolkit{c.end}")
    print(f"{c.gn}                  ---{c.end}")
    print(f"{c.cy}             Version{c.end} {c.gn}v2.0.0{c.end}")
    print(f"{c.bl}**************************************{c.end}")
    print(f"{c.inf}Checking information in '.env'...")
    try:
        if server_path==' 'or 'None':
            print(f"{c.fail}'SERVER_PATH' in the '.env' does not have a defined path! It must be set to your DCS Server Path where the DCS_server.exe is!{c.end}")
            t.sleep(10);return 0
        else: # Put this here to do what i wanted originally.
            print(f"{c.ok}Server Path set to: {server_path}{c.end}")
    except:    
            print(f"{c.fail}Couldn't locate the '.env' file. Make sure this program is in the same folder as it (or make it)!")
            t.sleep(10);return 0

    if disc.getHook()==False:
        print(f"{c.warn}Discord Webhook Usage Disabled!{c.end}")
        det.servinst()
    else:
        print(f"{c.ok}Discord Webhook Usage Enabled! Sending UP message!{c.end}")
        #disc.sendToolUP()
        det.servinst()

e.register(syS.safeexit)
