import win32con
import keyboard
import macros
import os
from configobj import ConfigObj

MACRO_PATH=os.path.dirname(os.path.abspath(macros.__file__))
ABORT_KEY=123 #F12
STOP_MACRO_KEY=160 #left shift button
PAUSE_KEY=114 #F3
REPEAT_KEY="" #Not currently used. Meant to be the toggle key for setting the repeat flag
REPEAT=True #If button is held down should the macro repeat itself?
PRINT=True
DELAY=.02 #the poll interval for keypress detection
PROFILE=ConfigObj(os.path.join(MACRO_PATH,'profiles.cfg'),list_values=False)
DEFAULT_PROFILE=os.path.join(MACRO_PATH,'dps.cfg')
