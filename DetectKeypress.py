import win32api
import win32con
import ctypes
import time
import mouse
import itertools
import keyboard as k
from keyboard import codes as c
from configobj import ConfigObj

try:
    filename="macroconfig.cfg"
    macroconfig=config=ConfigObj(filename,list_values=False)
except Exception as inst:
    print inst
    
def key_in_down_state(key_state):
    """Checks the passed in key state list of integers  or single integer. Returns True or False if all of them are in down state [-127,-128]"""
    
    in_down_state=lambda x: x in [-127,-128]
    
    if type(key_state)==list:
        return all([in_down_state(state) for state in key_state])
    else:
        return in_down_state(key_state)
    
def get_key_state(*args):
    """Runs the win32apiGetKeyState on the passed in args and returns them. """
    
    values=[]
    for arg in args:
        if type(arg)==tuple:
            return_value=[win32api.GetKeyState(n) for n in arg]
        else:
            return_value=win32api.GetKeyState(arg)
            
        values.append(return_value)
    return values

def get_triggers(dictionary):
    """
    Takes a macro dictionary and grabs all the triggers for a macro. Evaluates the trigger(string) returning a tupled number(s)
    """
    
    trigger_keys={}
    for macro in dictionary:
        keys=[]
        trigger_key=dictionary[macro].get('trigger').replace(' ','').split(',')
        for key in trigger_key:
            keys.append(k.codes.get(key))
        trigger_keys[macro]=tuple(keys)
        
    return trigger_keys


class KEYPRESS(object):
    
    def __init__(self,macro_dict,abort_key=win32con.VK_F12,pause_key=win32con.VK_F3,repeat_key=''):
        """
        Keypress detection. Fires a macro based on the keys it's looking for
        self.macro_hotkeys are keys(triggers) this function looks for to fire a macro, the structure is this:
        self.macro_hotkeys is a dictionary with a macroname key to look for pair. {'Macro Name':'virtual key','AttackMacro','win32con.VK_LCONTROL}
        'virtual key' is a  value representing a keyboard button or mouse button
        
        Abort key is the key it looks for break out of the main keypress detection loop (ends the function)
        Pause_key is the key to stop a macro from playing (pausing any new execution) but not exit the loop. A play toggle.
        """
                
        self.abort_key=abort_key
        self.pause_key=pause_key
        self.repeat_key=repeat_key
        self.macro_hotkeys=get_triggers(macro_dict)
        self.repeat=True
        self.print_output=True
        self.delay=.02        
        
        self.down_not_toggled=-127
        self.down_and_toggled=-128
        self.up_not_toggled=0
        self.up_and_toggled=1
        
        self.down_state=[self.down_not_toggled,self.down_and_toggled]
        self.up_state=[self.up_not_toggled,self.up_and_toggled]
        self.not_toggled=[self.up_not_toggled,self.down_not_toggled]
        self.toggled_on=[self.up_and_toggled,self.down_and_toggled]


    def keypress_detection(self):

        UpOrDownKeyState={}            
        abort_state=0       
        
        for item in self.macro_hotkeys:
            UpOrDownKeyState[item]=True
                    
        while not key_in_down_state(abort_state): #-127,-128 is returned by GetKeyState when the key passed to it is down
            for macro in self.macro_hotkeys:                
                abort_state,key_state,pause_state=get_key_state(self.abort_key,self.macro_hotkeys[macro],self.pause_key)
                if pause_state in self.not_toggled:pause=False
                elif pause_state in self.toggled_on:pause=True            
    
                playstate=UpOrDownKeyState.get(macro)
                
                if key_in_down_state(key_state)and playstate==True and pause==False: #key_state returns -127(down) or -128(down and toggled on) if key is being pressed
                    self.play_macro(macro)
                    if self.repeat==False:
                        UpOrDownKeyState[macro]=False #Only fire macro once while the key is being held down, Don't continually fire after done if key is being held down
                elif not key_in_down_state(key_state):#key in up state 
                    UpOrDownKeyState[macro]=True
                elif key_in_down_state(key_state) and self.print_output: print self.macro_hotkeys[macro],'Key is being held down'
            time.sleep(self.delay)#this is the poll interval how often should it check these keys?
        print 'Exiting'
    
    def play_macro(self,macroname):
        """
        Plays a Macro ie. a sequence of keystrokes and mouse clicks executes arbitary python code
        """
        
        macro=macroconfig[macroname]['actions']
        if self.print_output: print 'Starting:',macroname,'#############################################'
        for actionstring in macro:
            if self.print_output: print 'Executing:',actionstring,macro[actionstring]
            action=macro.get(actionstring)
            exec(action)
    
def main():
    KEYPRESS(macroconfig).keypress_detection()   
    
if __name__=='__main__':
    main()
