import pywinauto
import EnumerateWindows


def connect_to_window(window_name,ignore_case=True):
    """
    Connects to a window by the window name, returns a window or windows matching the name specified
    the window name doesn't have to be exact it'll pickup all windows with that name in the title
    If ignore case is true it'll ignore case when searching for windows
    """
    
    connected_windows=[]
    window_list=EnumerateWindows.get_windows_with_text(window_name,ignore_case)
    
    if window_list:
        for item in window_list:
            pwa_app = pywinauto.application.Application()
            try:
                w_handle = pywinauto.findwindows.find_windows(title=item)[0]
            except IndexError as e:
                print e,item
            else:
                window = pwa_app.window_(handle=w_handle)
                window.DrawOutline()
                connected_windows.append(window)
            
        if len(connected_windows)==1:
            return connected_windows[0]
        return connected_windows
    else:
        print 'No windows found with name: %s'%window_name
     