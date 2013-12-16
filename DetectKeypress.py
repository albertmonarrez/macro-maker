import win32api
import win32con
import ctypes
import time
import mousemacro
import random

try:
    filename="C:/pythonCustomCode/PythonWinService/macroconfig.cfg"
    macroconfig=config=ConfigObj(filename,list_values=False)
except Exception as inst:
    print inst

def keypress_detection(keysToLookFor,abort):
    """
    Keypress detection. Fires a macro based on the keys it's looking for
    keysToLookFor are keys(triggers) this function looks for to fire a macro, the structure is this:
    keysToLookFor is a dictionary with a macroname key to look for pair. {'Macro Name':'scancode key','AttackMacro','ord('H')'}
    'scancode key' should be ord(some letter) or a hex or number value representing a keyboard button or mouse button
    
    Abort key is the key it looks for break out of the main keypress detection loop (ends the function)
    """
    UpOrDownKeyState={}    
    keyIsDown=[-127,-128]
    pause=False    
    abortkey=''
    
    #Get Initial state of pause key is it 0 or 1 if one hit the pause key to make it zero
    pausekeyinitial=win32api.GetKeyState(win32con.VK_F3)
    if pausekeyinitial==0:
        pausekeyinitial=pausekeyinitial
    else:
        win32api.keybd_event(win32con.VK_F3,0,0,0)
        win32api.keybd_event(win32con.VK_F3,0,win32con.KEYEVENTF_KEYUP,0)        
    
    triggerMacroKeys=keysToLookFor
    for item in triggerMacroKeys:
        UpOrDownKeyState[item]=True
                
    while abortkey not in keyIsDown: #-127,-128 is returned by GetKeyState when the key passed to it is down
        for macro in triggerMacroKeys:                
            abortkey=win32api.GetKeyState(abort)#gets the state of the abort key returns either 0,1,-127,-128
            keyboardkey=triggerMacroKeys.get(macro)#returns a string from the config file with python representation of a key ex.win32con.VK_ESCAPE
            keyboardkey=eval(keyboardkey)#evaluates the python string
            keypressed=win32api.GetKeyState(keyboardkey)#gets the state of the look for key returns either 0,1,-127,-128
            pausekey=win32api.GetKeyState(win32con.VK_F3)
            
            if pausekey==0:
                pause=False
            elif pausekey==1:
                pause=True
            
            playstate=UpOrDownKeyState.get(macro)
            
            if keypressed in keyIsDown and playstate==True and pause==False: #keypressed returns -127 or -128 if key is being pressed
                #print keypressed,'Button is down.'
                play_macro(macro)
                UpOrDownKeyState[macro]=False #Only fire macro once while the key is being held down
            elif keypressed==0 or keypressed==1: #toggle state
                UpOrDownKeyState[macro]=True
                #print keypressed
            else: print triggerMacroKeys.get(macro),'Key is being held down'
        time.sleep(.02)
    print 'Exiting'

def play_macro(macroname):
    """
    Plays a Macro ie. a sequence of keystrokes and mouse clicks
    """
    
    macro=macroconfig[macroname]
    print 'Starting:',macroname,'#############################################'
    for actionstring in macro:
        print 'Executing:',actionstring,macro[actionstring]
        action=macro.get(actionstring)
        eval(action)
    
def main():
    triggerMacroKeys=macroconfig['triggers']
    keypress_detection(triggerMacroKeys,win32con.VK_F12) #look for h key then fire macro exit loop if escape key    
    
if __name__=='__main__':
    main()
