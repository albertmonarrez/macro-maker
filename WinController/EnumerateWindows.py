from win32com.client import Dispatch
import win32com.client
import win32gui
import ctypes
import win32ui


def outlook_read():
    session = win32com.client.gencache.EnsureDispatch ("MAPI.Session")    
    session.Logon("Outlook")
    
    return session

def enum_child_windows(handle):
    "Return a list of handles of the child windows of this handle"

    # this will be filled in the callback function
    child_windows = []

    # callback function for EnumChildWindows
    def EnumChildProc(hwnd, lparam):
        "Called for each child - adds child hwnd to list"

        # append it to our list
        child_windows.append(hwnd)

        # return true to keep going
        return True

    # define the child proc type
    enum_child_proc = ctypes.WINFUNCTYPE(
        ctypes.c_int, 			# return type
        ctypes.c_long, 	# the window handle
        ctypes.c_long)	# extra information

    # update the proc to the correct type
    proc = enum_child_proc(EnumChildProc)

    # loop over all the children (callback called for each)
    win32gui.EnumChildWindows(handle, proc, 0)

    return child_windows

def enum_windows():
    "Return a list of handles of all the top level windows"
    windows = []

    # The callback function that will be called for each HWND
    # all we do is append the wrapped handle
    def EnumWindowProc(hwnd, lparam):
        "Called for each window - adds handles to a list"
        windows.append(hwnd)
        return True

    # define the type of the child procedure
    enum_win_proc = ctypes.WINFUNCTYPE(
        ctypes.c_int, ctypes.c_long, ctypes.c_long)

    # 'construct' the callback with our function
    proc = enum_win_proc(EnumWindowProc)

    # loop over all the children (callback called for each)
    win32gui.EnumWindows(proc, 0)

    # return the collected wrapped windows
    return windows

def get_excel_stats():
    xl=Dispatch("Excel.Application")
    xl.Visible=True
    numberOfWorkbooks=xl.Workbooks.Count
    workbooks=xl.Workbooks
    
    print(xl,"Number of Workbooks:",numberOfWorkbooks)
    for item in workbooks:
        print('File name:',item.Name)
        xlbook=item
        for sheet in xlbook.Sheets:
            print('Sheet name:',sheet.Name)
        print('\n')
def get_window_by_name(windowTitle):
    x=win32ui.FindWindow(None,windowTitle)
    y=win32gui.FindWindow(None,windowTitle)
    
    return x,y
    
def get_windows_with_text(Text,ignore_case=True):
    windowNameList=[]
    all_windows=enum_windows()#returns a bunch of thread numbers in a list
    for item in all_windows:
        windowtext=win32gui.GetWindowText(item)
        if windowtext !='':#Don't print out empty strings    
            if ignore_case==True:
                Text=Text.lower()
                if Text in windowtext.lower():
                    windowNameList.append(windowtext)
            elif Text in windowtext:
                    windowNameList.append(windowtext)
                    
    return windowNameList


def get_window_names():
    all_windows=enum_windows()#returns a bunch of thread numbers in a list
    for item in all_windows:
        windowtext=win32gui.GetWindowText(item)
        if windowtext !='':#Don't print out empty strings
            print(windowtext,'Class:',win32gui.GetClassName(item))

    