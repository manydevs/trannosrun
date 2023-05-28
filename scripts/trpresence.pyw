from pypresence import Presence
import psutil
from tkinter.messagebox import showwarning as tromokratia
import time
import os
from contextlib import redirect_stdout


def cpr(p):
    for proc in psutil.process_iter():
        try:
            if p.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


if cpr('discord.exe') or cpr('discordptb.exe') or cpr('discordcanary.exe'):
    try:
        RPC = Presence(982695479731191878)
        RPC.connect()
    except:
        tromokratia("PyPresence: Connection Error", "PyPresence cannot hook to your Discord client.\n"
                                                    "This usually happens when you have no internet connection "
                                                    "and the Discord client is running.\n"
                                                    "TrannosRun will continue running now. To avoid errors like "
                                                    "this in the future, close all Discord instances before "
                                                    "running TrannosRun.")


        class RPC:
            def update(state, details, large_image, start):
                pass
else:
    class RPC:
        def update(state, details, large_image, start):
            pass

highscorecoords = os.getenv('APPDATA') + "\\TrannosRun\\highscore.ak47"
scorecoords = os.getenv('APPDATA') + "\\TrannosRun\\score.ak47"
epoch = int(time.time())
while True:
    if not os.path.isfile(os.getenv('APPDATA') + "\\TrannosRun\\playback.pass"):
        exit()
    if not os.path.isfile(highscorecoords):
        open(highscorecoords, "x")
        with open(highscorecoords, 'w') as f:
            with redirect_stdout(f):
                print(0)
        with open(highscorecoords) as f:
            getlastscore = int(f.read())
    else:
        with open(highscorecoords) as f:
            getlastscore = int(f.read())
    if cpr('discord.exe') or cpr('discordptb.exe') or cpr('discordcanary.exe'):
        RPC.update(state="Score: " + open(scorecoords, 'r').read().strip() + " | Highscore: " + str(getlastscore),
                   details="Listening to: " + open(os.getenv('APPDATA') + "\\TrannosRun\\currentmusic.ak47", "r").read().strip(),
                   large_image='http://cdn.discordapp.com/attachments/832302343268728903/982699191757312000/rpcicon.png',
                   start=epoch, large_text="v0.9.9")
