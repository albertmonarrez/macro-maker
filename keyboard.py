import collections
import time
import win32api

INPUT_KEYBOARD = 1
KEYEVENTF_EXTENDEDKEY = 1
KEYEVENTF_KEYUP       = 2
KEYEVENTF_UNICODE     = 4
KEYEVENTF_SCANCODE    = 8
VK_SHIFT        = 16
VK_CONTROL      = 17
VK_MENU         = 18

codes = collections.OrderedDict([
    ("A", 65),
    ("B", 66),
    ("C", 67),
    ("D", 68),
    ("E", 69),
    ("F", 70),
    ("G", 71),
    ("H", 72),
    ("I", 73),
    ("J", 74),
    ("K", 75),
    ("L", 76),
    ("M", 77),
    ("N", 78),
    ("O", 79),
    ("P", 80),
    ("Q", 81),
    ("R", 82),
    ("S", 83),
    ("T", 84),
    ("U", 85),
    ("V", 86),
    ("W", 87),
    ("X", 88),
    ("Y", 89),
    ("Z", 90),
    ("VK_LBUTTON",   1),
    ("VK_RBUTTON",   2),
    ("VK_MBUTTON",   4),
    ("VK_XBUTTON1",  5),
    ("VK_XBUTTON2",  6),
    ("VK_NUMPAD0",  96),
    ("VK_NUMPAD1",  97),
    ("VK_NUMPAD2",  98),
    ("VK_NUMPAD3",  99),
    ("VK_NUMPAD4", 100),
    ("VK_NUMPAD5", 101),
    ("VK_NUMPAD6", 102),
    ("VK_NUMPAD7", 103),
    ("VK_NUMPAD8", 104),
    ("VK_NUMPAD9", 105),
    ("VK_ACCEPT",   30),
    ("VK_ADD",     107),
    ("VK_APPS",     93),
    ("VK_ATTN",    246),
    ("VK_BACK",      8),
    ("VK_CANCEL",    3),
    ("VK_CAPITAL",  20),
    ("VK_CLEAR",    12),
    ("VK_CONTROL",  17),
    ("VK_CONVERT",  28),
    ("VK_CRSEL",   247),
    ("VK_DECIMAL", 110),
    ("VK_DELETE",   46),
    ("VK_DIVIDE",  111),
    ("VK_DOWN",     40),
    ("VK_END",      35),
    ("VK_EREOF",   249),
    ("VK_ESCAPE",   27),
    ("VK_EXECUTE",  43),
    ("VK_EXSEL",   248),
    ("VK_F1",      112),
    ("VK_F2",      113),
    ("VK_F3",      114),
    ("VK_F4",      115),
    ("VK_F5",      116),
    ("VK_F6",      117),
    ("VK_F7",      118),
    ("VK_F8",      119),
    ("VK_F9",      120),
    ("VK_F10",     121),
    ("VK_F11",     122),
    ("VK_F12",     123),
    ("VK_F13",     124),
    ("VK_F14",     125),
    ("VK_F15",     126),
    ("VK_F16",     127),
    ("VK_F17",     128),
    ("VK_F18",     129),
    ("VK_F19",     130),
    ("VK_F20",     131),
    ("VK_F21",     132),
    ("VK_F22",     133),
    ("VK_F23",     134),
    ("VK_F24",     135),
    ("VK_FINAL",   24),
    ("VK_HANGEUL",  21),
    ("VK_HANGUL",   21),
    ("VK_HANJA",    25),
    ("VK_HELP",     47),
    ("VK_HOME",     36),
    ("VK_INSERT",   45),
    ("VK_JUNJA",    23),
    ("VK_KANA",     21),
    ("VK_KANJI",    25),
    ("VK_LCONTROL",162),
    ("VK_LEFT",     37),
    ("VK_LMENU",   164),
    ("VK_LSHIFT",  160),
    ("VK_LWIN",     91),
    ("VK_MENU",        18),
    ("VK_MODECHANGE",  31),
    ("VK_MULTIPLY",   106),
    ("VK_NEXT",        34),
    ("VK_NONAME",     252),
    ("VK_NONCONVERT",  29),
    ("VK_NUMLOCK",    144),
    ("VK_OEM_CLEAR",  254),
    ("VK_PA1",        253),
    ("VK_PAUSE",       19),
    ("VK_PLAY",       250),
    ("VK_PRINT",       42),
    ("VK_PRIOR",       33),
    ("VK_PROCESSKEY", 229),
    ("VK_RCONTROL",   163),
    ("VK_RETURN",      13),
    ("VK_RIGHT",       39),
    ("VK_RMENU",      165),
    ("VK_RSHIFT",     161),
    ("VK_RWIN",        92),
    ("VK_SCROLL",     145),
    ("VK_SELECT",      41),
    ("VK_SEPARATOR",  108),
    ("VK_SHIFT",       16),
    ("VK_SNAPSHOT",    44),
    ("VK_SPACE",       32),
    ("VK_SUBTRACT",   109),
    ("VK_TAB",          9),
    ("VK_UP",          38),
    ("ZOOM",          251)])

def keybd_event(virtual_key,delay=.001,key_state='DownUp'):
    """
    A simplified version of win32api.keybd_event that's meant to take out some of the hassle of doing keydown keyup so it's less lines in
    the macro editor and simpler to edit. Simulates a keyboard event (pressing a key on the keyboard)
    Virual_key is an integer representing the key to be pressed ex. VK_XBUTTON1 =5. Delay is the time to wait after pressing a key down
    key_state is what you want to do with the key, press it (Down) release it (Up) press and release (DownUp) or do hot keys cntrl+a (Extend)
    
    """
    
    down=0
    
    if 'Down' in key_state:
        win32api.keybd_event(virtual_key,0,down,0)
        time.sleep(delay)
    elif 'Extend' in key_state:
        win32api.keybd_event(virtual_key,0,KEYEVENTF_EXTENDEDKEY,0)
        time.sleep(delay)
    if 'Up' in key_state:
        win32api.keybd_event(virtual_key,0,KEYEVENTF_KEYUP,0)
