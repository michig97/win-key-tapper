# press_win.py
# Windows-Taste per WinAPI SendInput auslösen (Tap/Down/Up)
# Usage:
#   python press_win.py --delay 10 --side left --mode tap
#   python press_win.py --mode down
#   python press_win.py --mode up

import time
import argparse
import ctypes
from ctypes import wintypes

user32 = ctypes.WinDLL("user32", use_last_error=True)

# INPUT types
INPUT_MOUSE = 0
INPUT_KEYBOARD = 1
INPUT_HARDWARE = 2

# Flags
KEYEVENTF_KEYUP = 0x0002

# VK codes
VK_LWIN = 0x5B
VK_RWIN = 0x5C

# Typfix für ULONG_PTR (Py < 3.11 robust)
if not hasattr(wintypes, "ULONG_PTR"):
    wintypes.ULONG_PTR = wintypes.WPARAM

class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx",          wintypes.LONG),
        ("dy",          wintypes.LONG),
        ("mouseData",   wintypes.DWORD),
        ("dwFlags",     wintypes.DWORD),
        ("time",        wintypes.DWORD),
        ("dwExtraInfo", wintypes.ULONG_PTR),
    ]

class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk",         wintypes.WORD),
        ("wScan",       wintypes.WORD),
        ("dwFlags",     wintypes.DWORD),
        ("time",        wintypes.DWORD),
        ("dwExtraInfo", wintypes.ULONG_PTR),
    ]

class HARDWAREINPUT(ctypes.Structure):
    _fields_ = [
        ("uMsg",    wintypes.DWORD),
        ("wParamL", wintypes.WORD),
        ("wParamH", wintypes.WORD),
    ]

class INPUTUNION(ctypes.Union):
    _fields_ = [
        ("mi", MOUSEINPUT),
        ("ki", KEYBDINPUT),
        ("hi", HARDWAREINPUT),
    ]

class INPUT(ctypes.Structure):
    _anonymous_ = ("u",)
    _fields_ = [
        ("type", wintypes.DWORD),
        ("u",    INPUTUNION),
    ]

SendInput = user32.SendInput
SendInput.argtypes = (wintypes.UINT, ctypes.POINTER(INPUT), ctypes.c_int)
SendInput.restype = wintypes.UINT

FindWindowW = user32.FindWindowW
FindWindowW.argtypes = (wintypes.LPCWSTR, wintypes.LPCWSTR)
FindWindowW.restype = wintypes.HWND

SetForegroundWindow = user32.SetForegroundWindow
SetForegroundWindow.argtypes = (wintypes.HWND,)
SetForegroundWindow.restype = wintypes.BOOL

def _send_inputs(inputs):
    arr = (INPUT * len(inputs))(*inputs)
    sent = SendInput(len(inputs), arr, ctypes.sizeof(INPUT))
    if sent != len(inputs):
        err = ctypes.get_last_error()
        raise OSError(err, f"SendInput sent {sent}/{len(inputs)} (error {err})")

def _focus_explorer_shell(delay_s: float = 0.08):
    # Fokus an Taskleiste/Explorer, damit Win-Ereignis sicher bei der Shell landet
    tray = FindWindowW("Shell_TrayWnd", None)
    if tray:
        SetForegroundWindow(tray)
        time.sleep(delay_s)

def win_down(vk):
    down = INPUT(type=INPUT_KEYBOARD)
    down.ki = KEYBDINPUT(wVk=vk, wScan=0, dwFlags=0, time=0, dwExtraInfo=0)
    _send_inputs([down])

def win_up(vk):
    up = INPUT(type=INPUT_KEYBOARD)
    up.ki = KEYBDINPUT(wVk=vk, wScan=0, dwFlags=KEYEVENTF_KEYUP, time=0, dwExtraInfo=0)
    _send_inputs([up])

def win_tap(vk, hold_ms=50):
    down = INPUT(type=INPUT_KEYBOARD)
    down.ki = KEYBDINPUT(wVk=vk, wScan=0, dwFlags=0, time=0, dwExtraInfo=0)
    up = INPUT(type=INPUT_KEYBOARD)
    up.ki = KEYBDINPUT(wVk=vk, wScan=0, dwFlags=KEYEVENTF_KEYUP, time=0, dwExtraInfo=0)
    _focus_explorer_shell()
    _send_inputs([down])
    time.sleep(hold_ms / 1000.0)
    _send_inputs([up])

def main():
    parser = argparse.ArgumentParser(
        description="Press the Windows key via WinAPI (tap/down/up) after a delay."
    )
    parser.add_argument("--delay", type=float, default=10, help="Delay in seconds (default: 10)")
    parser.add_argument("--side", choices=["left", "right"], default="left", help="Which Win key (default: left)")
    parser.add_argument("--mode", choices=["tap", "down", "up"], default="tap",
                        help="tap (press+release), or only down/up (default: tap)")
    parser.add_argument("--hold-ms", type=int, default=50, help="Hold duration for tap (ms)")
    args = parser.parse_args()

    vk = VK_LWIN if args.side == "left" else VK_RWIN

    time.sleep(args.delay)

    # Für alle Modi vorher die Shell fokussieren:
    _focus_explorer_shell()

    if args.mode == "tap":
        win_tap(vk, hold_ms=args.hold_ms)
    elif args.mode == "down":
        win_down(vk)
    elif args.mode == "up":
        win_up(vk)

if __name__ == "__main__":
    main()
