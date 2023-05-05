from pypresence import (Presence, DiscordNotFound)
import time
import os
from contextlib import redirect_stdout

try:
    RPC = Presence(982695479731191878)
    RPC.connect()
except DiscordNotFound:
    class RPC:
        def update(self, state, details, large_image, start, large_text):
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
    RPC.update(state="Score: " + open(scorecoords, 'r').read().strip() + " | Highscore: " + str(getlastscore),
               details="Listening to: " + open(os.getenv('APPDATA') + "\\TrannosRun\\currentmusic.ak47",
                                               "r").read().strip(),
               large_image='http://cdn.discordapp.com/attachments/832302343268728903/982699191757312000/rpcicon.png',
               start=epoch, large_text="v0.9.8-b")
