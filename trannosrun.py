import sys
import os
import subprocess
from contextlib import redirect_stdout
from urllib.request import urlretrieve as getfile
import requests
import shutil

from tkinter.messagebox import (showinfo, askokcancel)

if getattr(sys, 'frozen', False):
    truepath = os.path.dirname(sys.executable)
else:
    truepath = os.getcwd()

if os.path.isfile(truepath + "\\s-assets.zip"):
    os.remove(truepath + "\\s-assets.zip")


def startgame(hasmusic):
    if hasmusic:
        with redirect_stdout(open(truepath + "\\launcher.bat", "x")):
            print('@echo off\ncd scripts\n'
                  'start /b cmd /c ' + truepath + '\\env\\pythonw.exe ' + truepath + '\\scripts\\trgame.pyw\n'
                  'start /b cmd /c ' + truepath + '\\env\\pythonw.exe ' + truepath + '\\scripts\\trmusic.pyw\n'
                  'start /b cmd /c ' + truepath + '\\env\\pythonw.exe ' + truepath + '\\scripts\\trpresence.pyw')
    else:
        with redirect_stdout(open(truepath + "\\launcher.bat", "x")):
            print('@echo off\ncd scripts\n'
                  'start /b cmd /c ' + truepath + '\\env\\pythonw.exe ' + truepath + '\\scripts\\trgame.pyw\n'
                  'start /b cmd /c ' + truepath + '\\env\\pythonw.exe ' + truepath + '\\scripts\\trpresence.pyw')
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    subprocess.call(truepath + "\\silentcmd.exe " + truepath + "\\launcher.bat", startupinfo=si)
    os.remove(truepath + "\\launcher.bat")


try:
    response = requests.get("https://api.github.com/repos/manydevs/trannosrun/releases")
    tagname = ""
    index = 0
    while not tagname == "soundoutlet":
        tagname = response.json()[index]["tag_name"]
        index += 1
    index -= 1

    if not os.path.isfile(truepath + "\\soundver"):
        if not askokcancel("Music player cannot continue", "The sound library was not found.\n"
                                                           "Click OK to download it or Cancel to play without music."):
            startgame(False)
        else:
            showinfo("Connection established", "The requested library was found and will be downloaded after this"
                                               "infobox closes.\nNote: The sound library is quite large (~150MB), "
                                               "therefore you may have to wait up to 5 minutes for it to download.")
            getfile(response.json()[index]["assets"][0]["browser_download_url"], "s-assets.zip")
            if os.path.isdir(truepath + "\\scripts\\s-assets"):
                shutil.rmtree(truepath + "\\scripts\\s-assets")
            shutil.unpack_archive(truepath + "\\s-assets.zip", truepath + "\\scripts")
            os.remove(truepath + "\\s-assets.zip")
            with open(truepath + "\\soundver", "x") as wr:
                with redirect_stdout(wr):
                    print(response.json()[index]["name"])
            showinfo("Library downloaded", "The TrannosRun sound library has downloaded and unpacked successfully.\n"
                                           "Click OK to start the game.")
            startgame(True)

    elif not response.json()[index]["name"] == open(truepath + "\\soundver", "r").read().strip():
        if askokcancel("Outdated sound library", "The sound library has updated.\n"
                                                 "Click OK to download it or Cancel to play with the old one."):
            showinfo("Connection established", "The requested library was found and will be downloaded after this"
                                               "infobox closes.\nNote: The sound library is quite large (~150MB), "
                                               "therefore you may have to wait up to 5 minutes for it to download.")
            getfile(response.json()[index]["assets"][0]["browser_download_url"], "s-assets.zip")
            if os.path.isdir(truepath + "\\scripts\\s-assets"):
                shutil.rmtree(truepath + "\\scripts\\s-assets")
            shutil.unpack_archive(truepath + "\\s-assets.zip", truepath + "\\scripts")
            os.remove(truepath + "\\s-assets.zip")
            with open(truepath + "\\soundver", "w") as wr:
                with redirect_stdout(wr):
                    print(response.json()[index]["name"])
            showinfo("Library downloaded", "The TrannosRun sound library has downloaded and unpacked successfully.\n"
                                           "Click OK to start the game.")
            startgame(True)
        else:
            startgame(True)
    else:
        startgame(True)
except requests.exceptions.ConnectionError:
    if os.path.isdir(truepath + "\\scripts\\s-assets"):
        startgame(True)
    else:
        startgame(False)
