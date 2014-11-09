import win32api
import win32con
import ctypes
import time
import mouse
import itertools
import keyboard as k
from keyboard import codes as c
from configobj import ConfigObj

import config

    
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
    
    def __init__(self,macro_dict):
        """
        Keypress detection. Fires a macro based on the keys it's looking for
        self.macro_hotkeys are keys(triggers) this function looks for to fire a macro, the structure is this:
        self.macro_hotkeys is a dictionary with a macroname key to look for pair. {'Macro Name':'virtual key','AttackMacro','win32con.VK_LCONTROL}
        'virtual key' is a  value representing a keyboard button or mouse button
        
        Abort key is the key it looks for break out of the main keypress detection loop (ends the function)
        Pause_key is the key to stop a macro from playing (pausing any new execution) but not exit the loop. A play toggle.
        """
        
        #Configuration setup        
        self.abort_key=config.ABORT_KEY
        self.pause_key=config.PAUSE_KEY
        self.repeat_key=config.REPEAT_KEY
        self.repeat=config.REPEAT
        self.print_output=config.PRINT
        self.delay=config.DELAY
        self.reload=False
        self.pause=False
        
        #keystate key down, key up
        self.down_toggled_off=-127
        self.down_toggled_on=-128
        self.up_toggled_off=0
        self.up_toggled_on=1
        
        self.down_state=[self.down_toggled_off,self.down_toggled_on]
        self.up_state=[self.up_toggled_off,self.up_toggled_on]
        self.toggled_off=[self.up_toggled_off,self.down_toggled_off]
        self.toggled_on=[self.up_toggled_on,self.down_toggled_on]
        
        self.profiles=config.PROFILE
        if self.profiles:
            macro_dict.merge(self.profiles)
            
        self.macroconfig=macro_dict
        self.macro_hotkeys=get_triggers(macro_dict)
        
    def load_profile(self,file_name):
        """Loads or reloads a profile. file_name is the location to the macro. macro_dict is a ConfigObj that contains a list of macros the actions of those macros and the trigger key.
        This method sets self.macroconfig(the entire macro list) and self.macro_hotkeys(the trigger keys for the macos)"""
        
        macro_dict=ConfigObj(file_name,list_values=False)
        macro_dict.reload()
        if self.profiles:
            macro_dict.merge(self.profiles)
        self.macroconfig=macro_dict
        self.macro_hotkeys=get_triggers(macro_dict)
        
    def set_flag(self,key_state,flag):
        """Sets a particular class flag to true or false depending on the state it's in. Used for things like the pause flag to stop additional macro plays."""
        
        if key_state in self.toggled_off:
            setattr(self,flag,False)
        elif key_state in self.toggled_on:
            setattr(self,flag,True)
                       
    def keypress_detection(self):

        UpOrDownKeyState={}            
        abort_state=0       
        
        for item in self.macro_hotkeys:
            UpOrDownKeyState[item]=True
                    
        while not key_in_down_state(abort_state): 
            self.reload=False
            for macro in self.macro_hotkeys:
                playstate=UpOrDownKeyState.get(macro)                
                abort_state,key_state,pause_state=get_key_state(self.abort_key,self.macro_hotkeys[macro],self.pause_key)
                self.set_flag(pause_state,'pause')

                if key_in_down_state(key_state)and playstate==True and self.pause==False: 
                    self.play_macro(macro)
                    if self.repeat==False:UpOrDownKeyState[macro]=False #Only fire macro once while the key is being held down, Don't continually fire after done if key is being held down
                elif not key_in_down_state(key_state):#key in up state 
                    UpOrDownKeyState[macro]=True
                elif key_in_down_state(key_state) and self.print_output: print 'Paused',self.macro_hotkeys[macro],'Key is being held down'
                
                if self.reload:break #profile can set this to true to break out of the current statement
                
            time.sleep(self.delay)#this is the poll interval how often should it check these keys?
        print 'Exiting'
    
    def play_macro(self,macroname):
        """
        Plays a Macro ie. a sequence of keystrokes and mouse clicks executes arbitary python code
        If the stop macro key is pressed it stops execution of the rest of the macro.
        """
        
        macro=self.macroconfig[macroname]['actions']
        if self.print_output: print 'Starting:',macroname,'#############################################'
        for actionstring in macro:
            if self.print_output: print 'Executing:',actionstring,macro[actionstring]
            action=macro.get(actionstring)
            exec(action)
            if key_in_down_state(get_key_state(config.STOP_MACRO_KEY)):
                if self.print_output:print "Stopping macro because stop macro key(%s) was pressed."%config.STOP_MACRO_KEY
                break
    
def main():
    filename=config.DEFAULT_PROFILE
    macroconfig=ConfigObj(filename,list_values=False)
        
    KEYPRESS(macroconfig).keypress_detection()
    
if __name__=='__main__':
    main()
