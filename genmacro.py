#!python2.7
import time
from itertools import *
from configobj import ConfigObj


def show(filename):
    """Just opens and returns the file specified from the config object"""
    
    config=ConfigObj(filename,list_values=False)
    return config

def dictionary_to_list(dictionary):
    """Takes a macro dictionary from file and converts the macro actions dictionary to list, 
    essentially striping out all the keys leaving only the values"""
    
    for macro in dictionary:
        values=dictionary[macro]['actions'].values()
        dictionary[macro]['actions']=values
        
    return dictionary

def generate_macro(macro_dict,filename):
    """
    Writes out a macro file in .ini style. Takes a dictionary with this structure {triggers:{macroname:hotkey},macros:{macroname:[list of actions]}}
    Filename is the filename+path to write to.
    """
    
    config = ConfigObj(raise_errors=True,list_values=False)
    config.filename = filename
    
    for macro in macro_dict:
        config[macro]={}
        config[macro]['trigger']=macro_dict[macro]['trigger']
        config[macro]['actions']={}
        action_list=macro_dict[macro]['actions']#needs to be a list
        for item in izip(count(),action_list):
            config[macro]['actions']['action_%03d'%item[0]]=item[1]
            
    config.write()    
    
def main():
    print 'Main function'
    f="macroconfig.cfg"
    s=show(f)


if __name__=='__main__':
    s=main()
