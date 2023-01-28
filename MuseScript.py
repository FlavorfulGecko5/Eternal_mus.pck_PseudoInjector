from pywinauto import Application
from pywinauto import timings
import pyautogui
import os
import time

# Faster pywinauto GUI interaction time
timings.Timings.fast()

# Various pathway variables
START_DIR = os.getcwd()
PCK_PATH = os.path.join(START_DIR, "base", "sound", "soundbanks", "pc", "mus.pck")
XML_PATH = os.path.join(START_DIR, "base", "sound", "soundbanks", "pc", "muse_injector_working_xml.xml")

# Launch FusionTools and use first window
app = Application(backend="uia").start('FusionTools.exe') 
app["Basic Selector"]["Wwise Editor"].click()

# Second window - Load .pck file
app["Wwise Editor - Ready"]["Button4"].click()
app["Wwise Editor - Ready"]["Open fileDialog"].menu_select("Open file")
pyautogui.write(PCK_PATH)
pyautogui.press("enter")
app["Wwise Editor - Ready"]["Button6"].click()

# Third Window - Edit BNKs
app["Embedded BNKs"]["ListBox"].ListItem.click_input(button="right")
app["Embedded BNKs"]["Dialog2"].menu_select("Edit BNK")

# Fourth Window - Export XML Data (need new var because of duplicate window name)
fourth = app.window(title="Wwise Editor - Ready", active_only = True)
fourth["Button7"].click()
time.sleep(1)
fourth["Dialog"].menu_select("Export HIRC")
pyautogui.write(XML_PATH)
pyautogui.press("enter")

time.sleep(1)
os.remove(PCK_PATH)

# XML WRITING SHIT GOES HERE

# Fourth Window - Import modded XML
fourth["Button7"].click()
fourth["Dialog"].menu_select("Import HIRC")
pyautogui.write(XML_PATH)
pyautogui.press("enter")
time.sleep(1)
fourth["CloseButton"].click()
app["Embedded BNKs"]["CloseButton"].click()

# Second Window - Save modded .pck file
app["Wwise Editor - Ready"]["Button4"].click()
app["Wwise Editor - Ready"]["Open fileDialog"].menu_select("Save File")
pyautogui.write(PCK_PATH)
pyautogui.press("enter")
pyautogui.press("enter")
time.sleep(1)
app["Wwise Editor - Ready"]["CloseButton"].click()
app["Basic Selector"]["CloseButton"].click()