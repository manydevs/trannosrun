import subprocess
import os
import sys
from contextlib import redirect_stdout

if getattr(sys, 'frozen', False):
    truepath = os.path.dirname(sys.executable)
else:
    truepath = os.getcwd()

with open(os.getcwd() + "\\launcher.bat", "x") as f:
    with redirect_stdout(f):
        print('@echo off\n'
              'start /b cmd /c ' + truepath + '\\env\\pythonw.exe ' + truepath + '\\scripts\\trgame.pyw\n'
              'start /b cmd /c ' + truepath + '\\env\\pythonw.exe ' + truepath + '\\scripts\\trmusic.pyw\n'
              'start /b cmd /c ' + truepath + '\\env\\pythonw.exe ' + truepath + '\\scripts\\trpresence.pyw')

si = subprocess.STARTUPINFO()
si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
subprocess.call(truepath + "\\launcher.bat", startupinfo=si)
os.remove(truepath + "\\launcher.bat")
