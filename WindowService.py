import os
import win32service
import win32security
import win32process,win32con
import win32serviceutil
import time
import WindowService
import subprocess
import DetectKeypres
import win32api
import EnumerateWindows

#at this point. We're ready to go.
#Put simply, a python windows service inherits from win32serviceutils.ServiceFramework
#simply extending that class, sets up all you ever need to do.

class PythonWinService(win32serviceutil.ServiceFramework):
    _svc_name_ = "PythonWinService"
    _svc_display_name_ = "Python Windows Service"
    _svc_description_='Service that checks if DCUO is running'
    
    def __init__(self,args):
        win32serviceutil.ServiceFramework.__init__(self,args)
        #at this point service is created pefectly.
        #you could stop here and jump to setting up the '__main__' section,
        #but you wont be able to stop your service, and it won't do anything.
        #at the very least, you need to implement SvcDoRun() and better still SvcStop():
        #This next attribute is used when its stopping time.
        self.isAlive = True
        self.KeyPressInstance=False
    
    def SvcDoRun(self):
        import servicemanager
        while self.isAlive:
        #remember when i said you needed only two modules?
        #well... i think i lied. If you're going to do anything
        #usefull, you're going to obviously need more modules.
        #This next module servicemanager, has some funny
        #properties that makes it only to be visible when
        #the service is properly setup. This means it can't be imported
        #in normal python programs, and can't even be imported
        #in the Global Namespace, but only in local functions that
        #will be called after the service is setup. Anyway,
        #this module contains some utilities for writing to EventLog.
            #subprocess.Popen(r'"C:/Python27/python.exe" C:/pythonCustomCode/PythonWinService/DetectKeypres.py')
          
            DCwindow=EnumerateWindows.get_windows_with_text('DC Universe Online')
            servicemanager.LogInfoMsg('Looking for DC Universe instance %s' %DCwindow)
            if len(DCwindow)>0:
                servicemanager.LogInfoMsg('Found Running instance of DC Universe Online. %s' %DCwindow)
                print 'Found Running instance of DC Universe Online. %s' %DCwindow
                if self.KeyPressInstance==False:
                    servicemanager.LogInfoMsg('Turning on Keypress detection')
                    DetectKeypres.main()
                    self.KeyPressInstance==True

            servicemanager.LogInfoMsg("PythonWinService - is alive and Looking for stuff")
            #fpath="C:/Users/925rz8/Desktop/hello.py"
            #execfile(fpath)
            #os.startfile("C:/Users/925rz8/Desktop/Unity.3.x.Game.Development.Essentials.pdf")
            time.sleep(5)
        servicemanager.LogInfoMsg("PythonWinService - Stopped")
        
    def SvcStop(self):
        #before you stop, you'll want to inform windows that
        #you've recieved a stop signal, and you're trying to stop.
        #in the windows Service manager, this is what shows the status message as
        #'stopping'. This is important, since SvcDoRun() may take sometime before it stops.
        import servicemanager
        servicemanager.LogInfoMsg("PythonWinService - Recieved stop signal")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.isAlive = False #this will make SvcDoRun() break the while loop at the next iteration.
        self.KeyPressInstance=False
        
def ctrlHandler(ctrlType):
    return True

if __name__ == '__main__':
    win32api.SetConsoleCtrlHandler(ctrlHandler, True)
    win32serviceutil.HandleCommandLine(PythonWinService) #this line sets it all up to run properly.

