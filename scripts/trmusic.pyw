import os
import random
from contextlib import redirect_stdout
import sys

with redirect_stdout(open(os.devnull, 'w')):
    import pygame

soundloc = os.getcwd() + "\\s-assets"
globalvolume, fakevolume = 0.20, 20
with open(os.getenv('APPDATA') + "\\TrannosRun\\volume", "w") as vol:
    with redirect_stdout(vol):
        print(fakevolume)

pygame.mixer.init()
playlist = []
for path in os.listdir(soundloc):
    if os.path.isfile(os.path.join(soundloc, path)):
        path2 = path.replace(".mp3", "")
        playlist.append(path2)

ssel1 = playlist[random.randint(0, len(playlist) - 1)]
ssel2 = playlist[random.randint(0, len(playlist) - 1)]

mixer = pygame.mixer.Sound(os.getcwd() + "\\s-assets\\" + ssel1 + ".mp3")
mixer2 = pygame.mixer.Sound(os.getcwd() + "\\s-assets\\" + ssel2 + ".mp3")
soundmixdelay = int(mixer.get_length()) * 1000

mixer.set_volume(globalvolume)
mixer.play()
pygame.init()
SOUNDMIX = pygame.USEREVENT + 1
pygame.time.set_timer(SOUNDMIX, soundmixdelay)
localvar = True
if not os.path.isfile(os.getenv('APPDATA') + "\\TrannosRun\\currentmusic.ak47"):
    open(os.getenv('APPDATA') + "\\TrannosRun\\currentmusic.ak47", "x")

while True:
    if not os.path.isfile(os.getenv('APPDATA') + "\\TrannosRun\\playback.pass"):
        sys.exit()
    if localvar:
        if os.path.isfile(os.getenv('APPDATA') + "\\TrannosRun\\voldown"):
            if not fakevolume <= 0:
                fakevolume -= 10
                globalvolume -= 0.10
                mixer.set_volume(globalvolume)
                with open(os.getenv('APPDATA') + "\\TrannosRun\\volume", "w") as vol:
                    with redirect_stdout(vol):
                        print(fakevolume)
            os.remove(os.getenv('APPDATA') + "\\TrannosRun\\voldown")
        if os.path.isfile(os.getenv('APPDATA') + "\\TrannosRun\\volup"):
            if not fakevolume >= 100:
                fakevolume += 10
                globalvolume += 0.10
                mixer.set_volume(globalvolume)
                with open(os.getenv('APPDATA') + "\\TrannosRun\\volume", "w") as vol:
                    with redirect_stdout(vol):
                        print(fakevolume)
            os.remove(os.getenv('APPDATA') + "\\TrannosRun\\volup")

    else:
        with open(os.getenv('APPDATA') + "\\TrannosRun\\currentmusic.ak47", "w") as currm:
            with redirect_stdout(currm):
                print(ssel2)
        if os.path.isfile(os.getenv('APPDATA') + "\\TrannosRun\\voldown"):
            if not globalvolume == 0:
                fakevolume -= 10
                globalvolume -= 0.10
                mixer2.set_volume(globalvolume)
                with open(os.getenv('APPDATA') + "\\TrannosRun\\volume", "w") as vol:
                    with redirect_stdout(vol):
                        print(fakevolume)
            os.remove(os.getenv('APPDATA') + "\\TrannosRun\\voldown")
        if os.path.isfile(os.getenv('APPDATA') + "\\TrannosRun\\volup"):
            if not globalvolume == 1:
                fakevolume += 10
                globalvolume += 0.10
                mixer2.set_volume(globalvolume)
                with open(os.getenv('APPDATA') + "\\TrannosRun\\volume", "w") as vol:
                    with redirect_stdout(vol):
                        print(fakevolume)
            os.remove(os.getenv('APPDATA') + "\\TrannosRun\\volup")
    if os.path.isfile(os.getenv('APPDATA') + "\\TrannosRun\\skiptrack"):
        if localvar:
            ssel2 = playlist[random.randint(0, len(playlist) - 1)]
            while ssel1 == ssel2:
                ssel2 = playlist[random.randint(0, len(playlist) - 1)]
            mixer2 = pygame.mixer.Sound(os.getcwd() + "\\s-assets\\" + ssel2 + ".mp3")
            mixer2.set_volume(globalvolume)
            soundmixdelay = int(mixer2.get_length()) * 1000
            pygame.time.set_timer(SOUNDMIX, soundmixdelay)
            mixer2.play()
            mixer.stop()
            localvar = False
            with open(os.getenv('APPDATA') + "\\TrannosRun\\currentmusic.ak47", "w") as currm:
                with redirect_stdout(currm):
                    print(ssel2)

        elif not localvar:
            ssel1 = playlist[random.randint(0, len(playlist) - 1)]
            while ssel1 == ssel2:
                ssel1 = playlist[random.randint(0, len(playlist) - 1)]
            mixer = pygame.mixer.Sound(os.getcwd() + "\\s-assets\\" + ssel1 + ".mp3")
            mixer.set_volume(globalvolume)
            soundmixdelay = int(mixer.get_length()) * 1000
            pygame.time.set_timer(SOUNDMIX, soundmixdelay)
            mixer.play()
            mixer2.stop()
            localvar = True
            with open(os.getenv('APPDATA') + "\\TrannosRun\\currentmusic.ak47", "w") as currm:
                with redirect_stdout(currm):
                    print(ssel1)
                
        os.remove(os.getenv('APPDATA') + "\\TrannosRun\\skiptrack")
    for event in pygame.event.get():
        if event.type == SOUNDMIX:
            if localvar:
                ssel2 = playlist[random.randint(0, len(playlist) - 1)]
                while ssel1 == ssel2:
                    ssel2 = playlist[random.randint(0, len(playlist) - 1)]
                mixer2 = pygame.mixer.Sound(os.getcwd() + "\\s-assets\\" + ssel2 + ".mp3")
                mixer2.set_volume(globalvolume)
                soundmixdelay = int(mixer2.get_length()) * 1000
                pygame.time.set_timer(SOUNDMIX, soundmixdelay)
                mixer2.play()
                mixer.stop()
                localvar = False
                with open(os.getenv('APPDATA') + "\\TrannosRun\\currentmusic.ak47", "w") as currm:
                    with redirect_stdout(currm):
                        print(ssel2)

            elif not localvar:
                ssel1 = playlist[random.randint(0, len(playlist) - 1)]
                while ssel1 == ssel2:
                    ssel1 = playlist[random.randint(0, len(playlist) - 1)]
                mixer = pygame.mixer.Sound(os.getcwd() + "\\s-assets\\" + ssel1 + ".mp3")
                mixer.set_volume(globalvolume)
                soundmixdelay = int(mixer.get_length()) * 1000
                pygame.time.set_timer(SOUNDMIX, soundmixdelay)
                mixer.play()
                mixer2.stop()
                localvar = True
                with open(os.getenv('APPDATA') + "\\TrannosRun\\currentmusic.ak47", "w") as currm:
                    with redirect_stdout(currm):
                        print(ssel1)
