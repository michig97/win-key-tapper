# Win Key Tapper (Windows key via WinAPI)

Small utility to **press the Windows key in software** (left/right), optionally after a delay.
Useful if your keyboard's Win key is broken or for macro tooling.

- Uses **WinAPI SendInput** (robust)
- Modes: **tap**, **down**, **up**
- Select **left** or **right** Win key
- CLI args (`--delay`, `--side`, `--mode`, `--hold-ms`)
- Works with **Python** or a single-file **EXE** (PyInstaller)

> Windows only.

## Usage (Python)

1. Install Python 3.x on Windows (no extra pip deps).
2. Run from a normal (non-admin) terminal:

```bash
python press_win.py --delay 10 --side left --mode tap
```
# Beispiel-Batches
start_win_10s_tap.bat
```
@echo off
python "%~dp0press_win.py" --delay 10 --side left --mode tap
```
win_down.bat
```
@echo off
python "%~dp0press_win.py" --delay 0 --side left --mode down
```
win_up.bat
```
@echo off
python "%~dp0press_win.py" --delay 0 --side left --mode up
```
> [!TIP]
> Do **not** run elevated (as Administrator) unless Explorer is also elevated.  
> Some overlays/remappers may swallow the Win key; pause or disable them for testing.

---

## Troubleshooting

### Nothing happens
- Make sure you run **non-admin** if Explorer is non-admin.  
- Restart **Windows Explorer**  
  *(Task Manager → “Windows Explorer” → “Restart”)*.  
- Disable tools that capture the Win key  
  *(AHK hotkeys, game overlays, PowerToys, remappers)*.  
- **VMs** may intercept the Win key depending on host settings → test on real hardware.  
- **Policies/Kiosk mode** may block synthetic input at system level.





