import sys
import os
import subprocess
from contextlib import redirect_stdout
from urllib.request import urlretrieve as getfile
import requests
import shutil
from tkinter import (Checkbutton, Label, Tk, IntVar, Frame, Canvas, Scrollbar, BOTH, VERTICAL, Y, LEFT, RIGHT)
from tkinter.messagebox import (showinfo, askokcancel)

if getattr(sys, 'frozen', False):
    truepath = os.path.dirname(sys.executable)
else:
    truepath = os.getcwd()

if os.path.isfile(truepath + "\\s-assets.zip"):
    os.remove(truepath + "\\s-assets.zip")

with redirect_stdout(open(os.devnull, 'w')):
    getscreenres = Tk()
    screen_width, screen_height = int(getscreenres.winfo_screenwidth()), int(getscreenres.winfo_screenheight())
    getscreenres.destroy()


def startgame(hasmusic):
    if hasmusic:
        with redirect_stdout(open(truepath + "\\launcher.bat", "x")):
            print('@echo off\ncd scripts\n'
                  'start /b cmd /c ' + truepath +
                  '\\env\\pythonw.exe ' + truepath +
                  '\\scripts\\trgame.pyw\nstart /b cmd /c ' + truepath +
                  '\\env\\pythonw.exe ' + truepath +
                  '\\scripts\\trmusic.pyw\nstart /b cmd /c ' + truepath +
                  '\\env\\pythonw.exe ' + truepath +
                  '\\scripts\\trpresence.pyw')
    else:
        with redirect_stdout(open(truepath + "\\launcher.bat", "x")):
            print('@echo off\ncd scripts\n'
                  'start /b cmd /c ' + truepath +
                  '\\env\\pythonw.exe ' + truepath +
                  '\\scripts\\trgame.pyw\nstart /b cmd /c ' + truepath +
                  '\\env\\pythonw.exe ' + truepath +
                  '\\scripts\\trpresence.pyw')
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    subprocess.call(truepath + "\\silentcmd.exe " + truepath + "\\launcher.bat", startupinfo=si)
    os.remove(truepath + "\\launcher.bat")


def launch():
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
                                                               "Click OK to download it or Cancel to play without "
                                                               "music."):
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
                showinfo("Library downloaded", "The TrannosRun sound library has downloaded and unpacked "
                                               "successfully.\n "
                                               "Click OK to start the game.")
                gui()
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
                showinfo("Library downloaded", "The TrannosRun sound library has downloaded and unpacked "
                                               "successfully.\nClick OK to start the game.")
                gui()
            else:
                startgame(True)
        else:
            startgame(True)
    except requests.exceptions.ConnectionError:
        if os.path.isdir(truepath + "\\scripts\\s-assets"):
            startgame(True)
        else:
            startgame(False)


def gui():
    def center(query):
        global screen_width, screen_height
        query.update_idletasks()
        windowsize = tuple(int(_) for _ in query.geometry().split('+')[0].split('x'))
        x = screen_width / 2 - windowsize[0] / 2
        y = screen_height / 2 - windowsize[1] / 2
        query.geometry("+%d+%d" % (x, y))
    win = Tk()

    frm = Frame(win, bg='#87807E')
    frm.pack(fill=BOTH, expand=1)
    cnv = Canvas(frm, bg='#87807E')
    cnv.pack(side=LEFT, fill=BOTH, expand=1)
    scrollbar = Scrollbar(frm, orient=VERTICAL, command=cnv.yview, bg='#87807E')
    scrollbar.pack(side=RIGHT, fill=Y)
    cnv.configure(yscrollcommand=scrollbar.set)
    cnv.bind('<Configure>', lambda e: cnv.configure(scrollregion=cnv.bbox("all")))
    mainframe = Frame(cnv, width=1000, height=100, bg='#87807E')

    center(win)
    win.focus_force()
    win.configure(bg='#87807E')
    win.iconbitmap(truepath + '\\scripts\\assets\\mavro_jet.ico')
    win.title("TrannosRun Launcher")
    soundloc = truepath + "\\scripts\\s-assets"
    playlist = []
    Label(mainframe, text="TrannosRun Launcher",
          font="Consolas 21 bold", bg='#87807E').grid(column=0, row=0, columnspan=2)
    Label(mainframe, text="Select the songs you would\nlike to hear while in game.\n"
                          "This window will never show again,\nunless you press \"M\" while on the\ndeath screen.",
          font="Consolas 12 bold", bg='#87807E').grid(column=0, row=1, columnspan=2)

    for path in os.listdir(soundloc):
        if os.path.isfile(os.path.join(soundloc, path)) and ".mp3" in path:
            path2 = path.replace(".mp3", "")
            playlist.append(path2)

    ii = 2

    for i in playlist:
        Label(mainframe, text=i.replace("#", ""), font="Consolas 11", bg='#87807E')\
            .grid(sticky='w', column=1, row=ii)
        globals()["int" + str(ii)] = IntVar()
        globals()["ch" + str(ii)] = Checkbutton(mainframe, bg='#87807E', variable=globals()["int" + str(ii)])
        globals()["ch" + str(ii)].grid(column=0, row=ii)
        if "#" not in i:
            globals()["ch" + str(ii)].select()
        ii += 1

    def yes():
        for d in playlist:
            if globals()["int" + str(playlist.index(d) + 2)].get() == 0 and "#" not in d:
                os.rename(soundloc + "\\" + d + ".mp3", soundloc + "\\#" + d + ".mp3")
            if globals()["int" + str(playlist.index(d) + 2)].get() == 1 and "#" in d:
                os.rename(soundloc + "\\" + d + ".mp3", soundloc + "\\" + d.replace("#", "") + ".mp3")
        open(os.getenv('APPDATA') + "\\TrannosRun\\showplaylist.pass", "x")
        win.destroy()
        launch()

    win.protocol("WM_DELETE_WINDOW", yes)
    cnv.create_window((0, 0), window=mainframe, anchor="nw")

    win.mainloop()


if not os.path.isfile(os.getenv('APPDATA') + "\\TrannosRun\\showplaylist.pass") \
        and os.path.isdir(truepath + "\\scripts\\s-assets"):
    gui()
else:
    launch()
