import threading
import subprocess
import sys
import os
import time as t

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def stconsole():
    console_path = resource_path("console1.py")
    subprocess.run(["python", console_path])

def stmenu():
    menu_path = resource_path("menuz.py")
    subprocess.run(["python", menu_path])

if __name__ == "__main__":
    thread1 = threading.Thread(target=stconsole)
    thread2 = threading.Thread(target=stmenu)

    thread1.start()
    t.sleep(3)
    thread2.start()

    thread1.join()
    thread2.join()

    while thread2.is_alive()==True:
        pass
    else:
        print('Exit Received by User at Menu')
        sys.exit()
