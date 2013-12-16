import genmacro
import unittest
import os
import time
import mousemacro
from configobj import ConfigObj
from unittest import main

class TEST_UNIT_GENMACRO(unittest.TestCase):

    def test_show(self):
        filename="C:/pythonCustomCode/PythonWinService/macroconfig.cfg"
        f=genmacro.show(filename)
        self.assertIsNotNone(f.get('triggers'))
        print f
        
    def test_genmacro(self):
        path="C:/pythonCustomCode/PythonWinService/test_unit_genmacro.cfg"
        
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
        genmacro.generate_macro(macro_dict,path)
        self.assertTrue(os.path.exists(path))
        
        generated_file=genmacro.show(path)
        self.assertEqual(macro_dict.get('triggers'),generated_file.get('triggers'))
        lclaws=generated_file.get('LightClaws')
        claws=macro_dict.get('macros').get('LightClaws')
        self.assertIsNotNone(lclaws)
        self.assertIsNotNone(claws)