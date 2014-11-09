#!python2
import os
import time
import subprocess
import DetectKeypress
import win32api
from multiprocessing import Process
import WinController.EnumerateWindows as EnumerateWindows
import datetime

def find_game_instance():
    """Checks to see if DCUO is running if it is it starts the keypress detector."""
        
    while True:
        DCwindow=EnumerateWindows.get_windows_with_text('DC Universe Online [S')
        DCwindow2=EnumerateWindows.get_windows_with_text('DC Universe Online [T')
        if len(DCwindow)>0 or len(DCwindow2)>0:
            print 'Found Running instance of DC Universe Online. %s' %DCwindow
            p=Process(target=DetectKeypress.main,name='Keypresser')
            try:
                print'Turning on Keypress detection'
                p.start()
                p.join()#execution stops here and waits until this job is done before the loop continues.
                print 'After join',datetime.datetime.now()#testing to check the above is true
            except Exception as e:
                print e
                    
        time.sleep(2)
    print 'Service stopped'
        
if __name__ == '__main__':
    find_game_instance()

