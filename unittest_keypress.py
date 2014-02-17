import unittest
import itertools
import win32api
import win32con as w
import DetectKeypress
import keyboard
from configobj import ConfigObj
from keyboard import codes as c


class TEST_KEYPRESS(unittest.TestCase):
    
    def test_key_checking(self):
        testkeys=[(w.VK_LCONTROL,w.VK_LSHIFT,c.get('A')),
                  (w.VK_LCONTROL,w.VK_LSHIFT),
                  (c.get('B'),)
                  
                  ]
        
        state=DetectKeypress.get_key_state(w.VK_LCONTROL)
        self.assertIsNotNone(state)
        
        for keys in testkeys:
            for key in keys:
                keyboard.keybd_event(key,key_state='Down')
                
            state=DetectKeypress.get_key_state(keys)
            for key in keys:
                keyboard.keybd_event(key,key_state='Up')
            
            state=state[0]
            print state
            
            if 0 or 1 in state:
                self.fail("Key wasn't detected %s"%state)

    def test_key_depressed(self):
        false_list=[-1,0,[-127,-128,0],["-127",-128],'A']
        true_list=[-127,-128,[-127],[-128,-127],[-127,-128,-127,-128]]
        
        for num in false_list:
            self.assertFalse(DetectKeypress.key_in_down_state(num))
        for num2 in true_list:
                    self.assertTrue(DetectKeypress.key_in_down_state(num2))
                    
    def test_get_triggers(self):
        macroconfig=config=ConfigObj("macroconfig.cfg",list_values=False)
        trigs=DetectKeypress.get_triggers(macroconfig)
        for item in trigs.values():
            self.assertEqual(type(item),int)
            
        stringTrig=DetectKeypress.get_triggers(macroconfig,eval_num=False)
        for item in stringTrig.values():
                    self.assertEqual(type(item),str)       
        
        print trigs,stringTrig 
        
        