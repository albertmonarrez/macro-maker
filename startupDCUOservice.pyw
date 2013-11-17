import os
import time
import subprocess
import DetectKeypress
import win32api
import EnumerateWindows

def SvcDoRun():
    KeyPressInstance=False
    
    while True:
        DCwindow=EnumerateWindows.get_windows_with_text('DC Universe Online [S')
        DCwindow2=EnumerateWindows.get_windows_with_text('DC Universe Online [T')
        if len(DCwindow)>0 or len(DCwindow2)>0:
            print 'Found Running instance of DC Universe Online. %s' %DCwindow
            keypresswindow=EnumerateWindows.get_windows_with_text("C:\Windows\system32\cmd.exe")
            if not keypresswindow:
                try:
                    print'Turning on Keypress detection'
                    os.system("start /wait cmd /c C:/Python27/python.exe C:/pythonCustomCode/PythonWinService/DetectKeypress.py")
                except Exception,e:
                    print e
                    
        time.sleep(5)
    print 'Service stopped'
        
if __name__ == '__main__':
    SvcDoRun()

