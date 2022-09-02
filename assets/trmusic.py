import os, sys
import random
import psutil
import time
from tkinter.messagebox import showwarning as tromokratia
from contextlib import redirect_stdout
from pypresence import Presence

with redirect_stdout(open(os.devnull, 'w')):
    import pygame

try:
    os.chdir(sys._MEIPASS)
except AttributeError:
    pass


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

pygame.mixer.init()
playlist = ["Trannos, ATC Nico - AMG",
            "Trannos - Coco",
            "Trannos - Dolce",
            "Trannos - Ibiza",
            "Kings, Trannos - Madame",
            "Trannos, ATC Taff - Mauro Gyali",
            "Trannos, Billy Sio - MDMA",
            "Trannos, Light - Oplo",
            "Trannos - Industry",
            "Light, Trannos - 24hrs",
            "Trannos - Tropicana",
            "ATC Nico, Trannos - Studio",
            "FY, Light, Trannos - Obsessed",
            "Dirty Harry, Trannos - YAYO",
            "Leaderbrain, Trannos - Made In Albania",
            "Trannos, Eleni Foureira - Egw & Esy"]

ssel1 = playlist[random.randint(0, len(playlist) - 1)]
ssel2 = playlist[random.randint(0, len(playlist) - 1)]

mixer = pygame.mixer.Sound(os.getcwd() + "\\s-assets\\" + ssel1 + ".mp3")
mixer2 = pygame.mixer.Sound(os.getcwd() + "\\s-assets\\" + ssel2 + ".mp3")
soundmixdelay = int(mixer.get_length()) * 1000

mixer.set_volume(0.15)
mixer.play()
pygame.init()
SOUNDMIX = pygame.USEREVENT + 1
pygame.time.set_timer(SOUNDMIX, soundmixdelay)
localvar = True



while True:
    if not cpr('trannosrun.exe'):
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
    if localvar:
        if cpr('discord.exe') or cpr('discordptb.exe') or cpr('discordcanary.exe'):
            RPC.update(state="Score: " + open(scorecoords, 'r').read() + "| Highscore: " + str(getlastscore),
                       details="Listening to: " + ssel1,
                       large_image='http://cdn.discordapp.com/attachments/832302343268728903/982699191757312000/rpcicon.png',
                       start=epoch)
    else:
        if cpr('discord.exe') or cpr('discordptb.exe') or cpr('discordcanary.exe'):
            RPC.update(state="Score: " + open(scorecoords, 'r').read() + "| Highscore: " + str(getlastscore),
                       details="Listening to: " + ssel2,
                       large_image='http://cdn.discordapp.com/attachments/832302343268728903/982699191757312000/rpcicon.png',
                       start=epoch)
    for event in pygame.event.get():
        if event.type == SOUNDMIX:
            if localvar:
                ssel2 = playlist[random.randint(0, len(playlist) - 1)]
                while ssel1 == ssel2:
                    ssel2 = playlist[random.randint(0, len(playlist) - 1)]
                mixer2 = pygame.mixer.Sound(os.getcwd() + "\\s-assets\\" + ssel2 + ".mp3")
                soundmixdelay = int(mixer2.get_length()) * 1000
                pygame.time.set_timer(SOUNDMIX, soundmixdelay)
                mixer2.play()
                mixer.stop()
                localvar = False

            elif not localvar:
                ssel1 = playlist[random.randint(0, len(playlist) - 1)]
                while ssel1 == ssel2:
                    ssel1 = playlist[random.randint(0, len(playlist) - 1)]
                mixer = pygame.mixer.Sound(os.getcwd() + "\\s-assets\\" + ssel1 + ".mp3")
                soundmixdelay = int(mixer.get_length()) * 1000
                pygame.time.set_timer(SOUNDMIX, soundmixdelay)
                mixer.play()
                mixer2.stop()
                localvar = True
