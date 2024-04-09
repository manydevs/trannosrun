import os
import random
from contextlib import redirect_stdout
import sys

with redirect_stdout(open(os.devnull, 'w')):
    import pygame

soundloc = os.getcwd() + "\\s-assets"
globalvolume, fakevolume = 0.20, 20
with open(os.getenv('APPDATA') + "\\TrannosRun\\volume.info", "w") as vol:
    with redirect_stdout(vol):
        print(fakevolume)

pygame.mixer.init()
playlist = []
for path in os.listdir(soundloc):
    if os.path.isfile(os.path.join(soundloc, path)) and "#" not in path and ".mp3" in path:
        path2 = path.replace(".mp3", "")
        playlist.append(path2)

if len(playlist) == 0:
    sys.exit()
else:
    pback = playlist.copy()

random.shuffle(playlist)
ssel = playlist[0]
playlist.pop(0)

mixer = pygame.mixer.Sound(os.getcwd() + "\\s-assets\\" + ssel + ".mp3")
soundmixdelay = int(mixer.get_length()) * 1000

mixer.set_volume(globalvolume)
mixer.play()
with open(os.getenv('APPDATA') + "\\TrannosRun\\currentmusic.info", "w") as currm:
    with redirect_stdout(currm):
        print(ssel)
pygame.init()
SOUNDMIX = pygame.USEREVENT + 1
pygame.time.set_timer(SOUNDMIX, soundmixdelay)

while True:
    if not os.path.isfile(os.getenv('APPDATA') + "\\TrannosRun\\playback.pass"):
        sys.exit()
    if len(playlist) == 0:
        playlist = pback.copy()
        random.shuffle(playlist)

    if os.path.isfile(os.getenv('APPDATA') + "\\TrannosRun\\voldown.pass"):
        if not fakevolume <= 0:
            fakevolume -= 10
            globalvolume -= 0.10
            mixer.set_volume(globalvolume)
            with open(os.getenv('APPDATA') + "\\TrannosRun\\volume.info", "w") as vol:
                with redirect_stdout(vol):
                    print(fakevolume)
        try:
            os.remove(os.getenv('APPDATA') + "\\TrannosRun\\voldown.pass")
        except PermissionError:
            pass

    if os.path.isfile(os.getenv('APPDATA') + "\\TrannosRun\\volup.pass"):
        if not fakevolume >= 100:
            fakevolume += 10
            globalvolume += 0.10
            mixer.set_volume(globalvolume)
            with open(os.getenv('APPDATA') + "\\TrannosRun\\volume.info", "w") as vol:
                with redirect_stdout(vol):
                    print(fakevolume)
        try:
            os.remove(os.getenv('APPDATA') + "\\TrannosRun\\volup.pass")
        except PermissionError:
            pass

    if os.path.isfile(os.getenv('APPDATA') + "\\TrannosRun\\skiptrack.pass"):
        ssel = playlist[0]
        playlist.pop(0)
        mixer.stop()
        mixer = pygame.mixer.Sound(os.getcwd() + "\\s-assets\\" + ssel + ".mp3")
        mixer.set_volume(globalvolume)
        soundmixdelay = int(mixer.get_length()) * 1000
        pygame.time.set_timer(SOUNDMIX, soundmixdelay)
        mixer.play()
        with open(os.getenv('APPDATA') + "\\TrannosRun\\currentmusic.info", "w") as currm:
            with redirect_stdout(currm):
                print(ssel)
        os.remove(os.getenv('APPDATA') + "\\TrannosRun\\skiptrack.pass")

    for event in pygame.event.get():
        if event.type == SOUNDMIX:
            ssel = playlist[0]
            playlist.pop(0)
            mixer.stop()
            mixer = pygame.mixer.Sound(os.getcwd() + "\\s-assets\\" + ssel + ".mp3")
            mixer.set_volume(globalvolume)
            soundmixdelay = int(mixer.get_length()) * 1000
            pygame.time.set_timer(SOUNDMIX, soundmixdelay)
            mixer.play()
            with open(os.getenv('APPDATA') + "\\TrannosRun\\currentmusic.info", "w") as currm:
                with redirect_stdout(currm):
                    print(ssel)
