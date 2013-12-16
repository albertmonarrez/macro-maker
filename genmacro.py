import time
import mousemacro
from configobj import ConfigObj


def show(filename):
    """Just opens and returns the file specified from the config object"""
    
    config=ConfigObj(filename)
    return config
    
def generate_macro(macro_dict,filename):
    """
    Writes out a macro file in .ini style. Takes a dictionary with this structure {triggers:{macroname:hotkey},macros:{macroname:[list of actions]}}
    Filename is the filename+path to write to.
    """
    
    config = ConfigObj()
    config.filename = filename
    #
    triggers=macro_dict.get('triggers')
    config['triggers'] = triggers
    
    macros=macro_dict.get('macros')
    for macro in macros:
        action_list=macros.get(macro)
        config[macro]={}
        for item in action_list:
            config[macro]['action_%03d'%action_list.index(item)]=item
            
    config.write()    
    
def make_dictionary(triggers,macro):
    pass
    
def main():
    print 'Main function'
    f="C:/pythonCustomCode/PythonWinService/macroconfig.cfg"
    s=show(f)
    macro_dict={
    'triggers':{'LightClaws': 'win32con.VK_XBUTTON1', 'Macro2': 'win32con.VK_MBUTTON', 'Macro3': 'win32con.VK_NUMPAD1', 'Macro4': 'win32con.VK_NUMPAD2'},
    'macros':{'LightClaws':
            ['time.sleep(.45)',
            'mousemacro.hold()',
            'time.sleep(.4)',
            'win32api.keybd_event(ord(\'2\'), ord(\'2\'), 0, 0)',
            'win32api.keybd_event(ord(\'2\'), ord(\'2\'), win32con.KEYEVENTF_KEYUP, 0)', 
            'time.sleep(.2)',
            'mousemacro.release()', 
            'time.sleep(.3)', 
            'mousemacro.click()', 
            'time.sleep(.2)', 
            'mousemacro.click()', 
            'time.sleep(.07)']}
    }
    
    generate_macro(macro_dict,"C:/pythonCustomCode/PythonWinService/gentest.cfg")
    return s


if __name__=='__main__':
    s=main()