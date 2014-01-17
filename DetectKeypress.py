import win32api
import win32con
import ctypes
import time
import mousemacro
import random
from configobj import ConfigObj

try:
    filename="macroconfig.cfg"
    macroconfig=config=ConfigObj(filename,list_values=False)
except Exception as inst:
    print inst
    
def get_key_state(*args):
    """Runs the win32apiGetKeyState on the passed in args and returns them. """
    
    values=[]
    for arg in args:
        return_value=win32api.GetKeyState(arg)
        values.append(return_value)
    
    return values

def get_triggers(dictionary):
    trigger_keys={}
    for macro in dictionary:
        trigger_keys[macro]=dictionary[macro].get('trigger')
        
    return trigger_keys
            
def keypress_detection(keysToLookFor,abort,pausekey):
    """
    Keypress detection. Fires a macro based on the keys it's looking for
    keysToLookFor are keys(triggers) this function looks for to fire a macro, the structure is this:
    keysToLookFor is a dictionary with a macroname key to look for pair. {'Macro Name':'virtual key','AttackMacro','ord('H')'}
    'virtual key' is a  value representing a keyboard button or mouse button
    
    Abort key is the key it looks for break out of the main keypress detection loop (ends the function)
    """
    
    UpOrDownKeyState={}    
    down_not_toggled=-127
    down_and_toggled=-128
    up_not_toggled=0
    up_and_toggled=1
    
    down_state=[down_not_toggled,down_and_toggled]
    up_state=[up_not_toggled,up_and_toggled]
    not_toggled=[up_not_toggled,down_not_toggled]
    toggled_on=[up_and_toggled,down_and_toggled]
    
    abortkey=''
    
    #press pause key to get the toggle state is it 0 or 1 if one hit the pause key to reset to zero
    win32api.keybd_event(pausekey,0,0,0)
    if win32api.GetKeyState(pausekey)==down_and_toggled:
        win32api.keybd_event(pausekey,0,win32con.KEYEVENTF_KEYUP,0)        

    for item in keysToLookFor:
        UpOrDownKeyState[item]=True
        keysToLookFor[item]=eval(keysToLookFor.get(item))
                
    while abortkey not in down_state: #-127,-128 is returned by GetKeyState when the key passed to it is down
        for macro in keysToLookFor:                
            abortkey,keypressed,pause_state=get_key_state(abort,keysToLookFor[macro],pausekey)
            if pause_state in not_toggled:pause=False
            elif pause_state in toggled_on:pause=True            

            playstate=UpOrDownKeyState.get(macro)
            
            if keypressed in down_state and playstate==True and pause==False: #keypressed returns -127(down) or -128(down and toggled on) if key is being pressed
                play_macro(macro)
                UpOrDownKeyState[macro]=False #Only fire macro once while the key is being held down, Don't continually fire after done if key is being held down
            elif keypressed in up_state: 
                UpOrDownKeyState[macro]=True
            elif keypressed in down_state: print keysToLookFor[macro],'Key is being held down'
        time.sleep(.02)
    print 'Exiting'

def play_macro(macroname):
    """
    Plays a Macro ie. a sequence of keystrokes and mouse clicks
    """
    
    macro=macroconfig[macroname]['actions']
    print 'Starting:',macroname,'#############################################'
    for actionstring in macro:
        print 'Executing:',actionstring,macro[actionstring]
        action=macro.get(actionstring)
        exec(action)
    
def main():
    triggerMacroKeys=get_triggers(macroconfig)
    keypress_detection(triggerMacroKeys,win32con.VK_F12,win32con.VK_F3) #look for h key then fire macro exit loop if escape key    
    
if __name__=='__main__':
    main()

#[key for key in keypressed if key in down_state]==keypressed
