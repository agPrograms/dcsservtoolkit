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
webhook_url: str = os.getenv('WEBHOOK_URL')
server_path: str = os.getenv('SERVER_PATH')
useDiscord: bool = False # thinking of moving this to the .env
# BUG 1: Squashed, https from requests crashes program when calling webhook_url with an invalid url. Added try & exception to catch and continue.
# BUG 2: Squashed, unable to call first arguement at e.register. extra parathises.

global dcs
#global color
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
    def safeexit():
        #if det.procfind()==False or '': 
        print(f"{c.warn}!***PROGRAM IS TERMINATING***!{c.end}")
        print(f"{c.ok}Sending Down Message and Exiting Safely!{c.end}")
        global dataUP
        dataUP = {
            "content:": "😴 DCS Server Toolkit is exiting. Your server may also be going down too! ⚠️"
        }
        try:
            r.post(webhook_url, json=dataUP)
        except:
            print(f"{c.fail}COULD NOT SEND MESSAGE DUE TO: INVALID WEBHOOK URL!{c.end}")
        t.sleep(3);return 0

class det:
    def servinst(): # First call to grab/check the server process. If its not already running, we try to execute it.
        print(f"{c.ok}Started at {getTime:%H:%M:%S}{c.end}")
        print(f"{c.inf}Looking for DCS Server..{c.end}")
        if det.procfind(dcs) == True:
            print(f"{c.ok}DCS Server is running!{c.end}")
            if useDiscord:disc.sendServUP()
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
            subprocess.call([str(server_path)+'\\'+dcs]) # might not need to make server_path to string. But it could be a NoneType when it hits here...
        except:
            print(f"{c.fail}Could not start "+dcs+f". Please make sure 'SERVER_PATH' is set correctly in '.env'!{c.end}")
            print(f"{c.fail}Current Path: '"+str(server_path)+f"'{c.end}")
            if useDiscord:disc.sendCNS()
            t.sleep(10);return 0
        t.sleep(15);det.servmon()

    def servmon(): # Monitor the process of the server executable. Check every 60 seconds.
        if det.procfind(dcs)==False or '':
            print(f"{c.warn}DCS Server is down. Restarting in 3 seconds...")
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
        r.post(webhook_url, json=dataUP)
        try:
            r.post(webhook_url, json=dataUP)
        except:
            print(f"{c.warn}The 'WEBHOOK_URL' set in '.env' is not valid! Failed to send message to discord! Continuing...{c.end}")

    def sendServUP():
        global dataUP
        dataUP = {
            "content": "The DCS Server is up! 👅"
        }
        r.post(webhook_url, json=dataUP)
        try:
            r.post(webhook_url, json=dataUP)
        except:
            print(f"{c.warn}The 'WEBHOOK_URL' set in '.env' is not valid! Failed to send message to discord! Continuing...{c.end}")

    def sendToolUP():
        global dataUP
        dataUP = {
            "content": "DCS Server Toolkit is **Operational** and running **Version v1.1.0**.. Getting your server started! 😍"
        }
        r.post(webhook_url, json=dataUP)
        try:
            r.post(webhook_url, json=dataUP)
        except:
            print(f"{c.warn}The 'WEBHOOK_URL' set in '.env' is not valid! Failed to send message to discord! Continuing...{c.end}")

    def getHook():
        global useDiscord
        try:
            if webhook_url=='':
                print(f"{c.warn}Invalid or no webhook defined in '.env'!{c.end}")
                useDiscord = False # This might not be needed here. Need to do more testing.
                return False
            else:
                print(f"{c.ok}Discord Webhook set to: "+webhook_url+f"{c.end}")
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
    print(f"{c.cy}             Version{c.end} {c.gn}v1.1.0{c.end}")
    print(f"{c.bl}**************************************{c.end}")
    print
    print(f"{c.inf}Checking information in '.env'...")
    try:
        if server_path=='':
            print(f"{c.fail}'SERVER_PATH' in the '.env' does not have a defined path! It must be set to your DCS Server Path where the DCS_server.exe is!{c.end}")
            t.sleep(10);return 0
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
