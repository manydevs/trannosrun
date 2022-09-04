import subprocess
from contextlib import redirect_stdout
import time
import os
import sys

if getattr(sys, 'frozen', False):
    truepath = os.path.dirname(sys.executable)
else:
    truepath = os.getcwd()

with open(os.getcwd() + "\\trnsnd.bat", "x") as f:
    with redirect_stdout(f):
        print('@echo off\ncd scripts\n'
              'start /b cmd /c "' + str(truepath) + '\\env\\pythonw.exe" "' + str(truepath) + '\\scripts\\trmusic.pyw"\n'
              'start /b cmd /c "' + str(truepath) + '\\env\\pythonw.exe" "' + str(truepath) + '\\scripts\\trgame.pyw"')

si = subprocess.STARTUPINFO()
si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
subprocess.call(truepath + "\\trnsnd.bat", startupinfo=si)

time.sleep(1)
os.remove(truepath + "\\trnsnd.bat")
