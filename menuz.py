import dearpygui.dearpygui as dpg
import os
import subprocess
import sys
import time as t
from dotenv import load_dotenv

load_dotenv('.env')
server_path: str = os.getenv('SERVER_PATH')
dcs = 'DCS_server.exe'
#writepath = server_path
#if str(server_path) == '': write_path = "No Path Found!"

def exitTool():
    os.system(f"taskkill /F /IM Python.exe") # will be replaced soon.

def goodbye():
    os.system(f"taskkill /im {dcs}")
    t.sleep(3)
    return 0 # this might not work.
def repair():
    subprocess.Popen(['powershell.exe', f'Set-Location "{server_path}"; ./dcs_updater.exe @openbeta repair; exit'])
    pass

def update():
    subprocess.Popen(['powershell.exe', f'Set-Location "{server_path}"; ./dcs_updater.exe @openbeta update; exit'])
    pass

dpg.create_context()
dpg.create_viewport(title='DCS Server Toolkit Menu', width=650, height=350)

with dpg.window(tag="MAIN_Win"):
    dpg.add_text("Version v2.0.0")
    dpg.add_text("______________________________________")
    #dpg.add_spacer(height=2)
    dpg.add_text(f"Current Server Path: {server_path}")
    dpg.add_spacer(height=15)
    with dpg.group(horizontal=True):
        dpg.add_button(label="Update Server", tag='update',callback=update)
        dpg.add_button(label="Repair Server", tag='repair',callback=repair)
        dpg.add_button(label="Close Server", tag='exit',callback=goodbye)
    dpg.add_spacer(height=70)
    dpg.add_button(label="Force Exit Tool", tag='exitT',callback=exitTool)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("MAIN_Win", True)
dpg.start_dearpygui()
dpg.destroy_context()
