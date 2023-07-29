import subprocess
import colorama
from datetime import datetime
import time as t
colorama.init(wrap=True)

global dcs
global color
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

class det:
    def servinst(): # First call to grab/check the server process. If its not already running, we try to execute it.
        print(f"{c.ok}Started at {getTime:%H:%M:%S}{c.end}")
        print(f"{c.inf}Looking for DCS Server..{c.end}")
        if det.procfind(dcs) == True:
            print(f"{c.ok}DCS Server is running!{c.end}")
            det.servmon()
        else:
            print(f"{c.warn}DCS Server is not running.{c.end}")
            det.servstart()

    def procfind(serv_name): # Grab the process from the machine tasklist. Will return the value of the process as a string.
        call = 'TASKLIST', '/FI', 'imagename eq %s' % serv_name
        output = subprocess.check_output(call).decode()
        last_line = output.strip().split('\r\n')[-1]
        return last_line.lower().startswith(serv_name.lower())
    
    def servstart(): # Start the server from the order of a nother function. Catch errors if they pop up.
        print(f"{c.inf}Starting DCS Server...{c.end}")
        try:
            subprocess.call([pstr+'\\DCS_server.exe'])
        except:
            print(f"{c.fail}Could not start 'DCS_server.exe'. Please make sure 'path.txt' is set to the correct path!")
            t.sleep(10);return 0
        t.sleep(15);det.servmon()

    def servmon(): # Monitor the process of the server executable. Check every 60 seconds.
        if det.procfind(dcs)==False or '':
            print(f"{c.warn}DCS Server is down. Restarting in 3 seconds...")
            t.sleep(3);det.servstart()
        else:
            t.sleep(60)
            det.servmon() # theres totally a cleaner way to do this. Bad practice, I know.


# Prints log window and banner. Make it pretty cause why not. Using lambda cause calling a function within a class is dumb for this.
@lambda _: _()
def func() -> str:
    print(f"{c.bl}**************************************{c.end}")
    print(f"{c.cy}     DCS Server Essentials Toolkit{c.end}")
    print(f"{c.gn}                  ---{c.end}")
    print(f"{c.cy}             Version{c.end} {c.gn}v1.0.0{c.end}")
    print(f"{c.bl}**************************************{c.end}")
    print(f"{c.inf}Checking path defined in 'path.txt'...")
    try: # Get path.txt file. If no file exists, issue an error. Set pstr as '' to trigger statement so it doesnt error out. Else continue.
        with open ('path.txt', 'r') as file:
            global pstr
            pstr = str(file.read())
    except:
            print(f"{c.fail}Couldn't locate the 'path.txt' file. Make sure this program is in the same folder as it (or make it)!")
            t.sleep(3);pstr=''
            if pstr == '':
                print(f"{c.fail}PATH NOT DEFINED. DEFINE SERVER PATH IN 'path.txt'!{c.end}")
                t.sleep(10);return 0
            else:print(f"{c.ok}Server path set to: "+pstr +f"{c.end}");det.servinst()