from lxml import etree
from pywinauto import Application
from pywinauto import timings
import pyautogui
import os
import sys
import time

# Faster pywinauto GUI interaction time
timings.Timings.fast()

# Various important constant variables
START_DIR = os.getcwd()
PCK_PATH = os.path.join(START_DIR, "base", "sound", "soundbanks", "pc", "mus.pck")
XML_PATH = os.path.join(START_DIR, "base", "sound", "soundbanks", "pc", "muse_injector_working_xml.xml")
MODS_PATH = "xmls"
MODFILES = os.listdir(MODS_PATH)

# Early-exit if mod folder is empty
print("Found " + str(len(MODFILES)) + " potential mus.pck mod files")
#if len(MODFILES) == 0:
#    print("Terminating without injecting mods.")
#    sys.exit(0)

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

# Parse all XML files
xmlPack = etree.parse(XML_PATH)
for modfileName in MODFILES:
    print("Parsing mod file '" + modfileName + "'")
    idDict = {}
    xmlMod = etree.parse(os.path.join(MODS_PATH, modfileName))
    xmlObjects = xmlMod.xpath("/PCKMod/object")
    for obj in xmlObjects:
        for prop in obj:
            if prop.get("name") == "ID":
                id = prop.get("value")
                if id in idDict:
                    print("     WARNING - Duplicate HIRC object ID " + id + " - Ignoring duplicate entry")
                else:
                    idDict.update({id : obj})
    xmlPackObjects = xmlPack.xpath("/Data/HIRC/object")
    for packObj in xmlPackObjects:
        for packProp in packObj:
            if packProp.get("name") == "ID":
                id = packProp.get("value")
                if id in idDict:
                    packObj.getparent().replace(packObj, idDict[id])

# lxml auto-collapses empty tags (i.e. <derp></derp> --> <derp/>)
# In a vanilla mus.pck xml, there are no empty, uncollapsed tags except for the <BNKName> in <Metadata>
# If this tag is collapsed, FusionTools throws an error when importing
# This line prevent this auto-collapse
xmlPack.xpath("/Data/MetaData/BNKName")[0].text = ''

# Write the modded XML file
xmlPack.write(XML_PATH, pretty_print=True, xml_declaration=True, encoding="UTF-8")

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

sys.exit(0)