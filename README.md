# keylogger-heatmap
Simple Keylogger with statistics functionalities

pyinstaller .\keylogger.py --workpath ".\build\build\" --distpath ".\build\dist\" -w --hidden-import "pynput.keyboard._win32" --hidden-import "pynput.mouse._win32"