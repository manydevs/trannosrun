import os
import random
import sys as system
import string
from urllib.request import urlretrieve as getfile
from contextlib import redirect_stdout
from tkinter import *
from tkinter.filedialog import (askopenfilename, askdirectory)
from tkinter.messagebox import (askyesno, showinfo, askyesnocancel, showerror, showwarning)
import requests
import ctypes
from ctypes import wintypes
import uuid
import hashlib
import pygame
import redis
from time import (sleep, time)
from threading import Thread
import pypresence
from tqdm.auto import tqdm
import re

from pygame.locals import \
    K_w, \
    K_a, \
    K_s, \
    K_d, \
    K_c, \
    K_v, \
    K_g, \
    K_LSHIFT, \
    K_RSHIFT, \
    K_UP, \
    K_DOWN, \
    K_LEFT, \
    K_RIGHT, \
    K_ESCAPE, \
    KEYDOWN, \
    QUIT

try:
    import pyi_splash

    pyi_splash.close()
except ModuleNotFoundError:
    pass

if getattr(system, 'frozen', False):
    thispath = os.path.dirname(system.executable)
    meipath = system._MEIPASS
    if system.argv[0] == thispath + "\\setup.exe":
        showwarning("TrannosRun Migration Dialog", "TrannosRun detected that you updated from a 1.0.x version.\n\n"
                                                   "The new version of the game functions from a "
                                                   "single executable, meaning that there is no need to keep "
                                                   "TrannosRun installed as an app.\n\n"
                                                   "It is recommended that you delete "
                                                   "the %LocalAppData%\\Programs\\TrannosRun "
                                                   "folder (to delete the old track library).\n\n"
                                                   "Please download TrannosRun again from the ManyDevs' GitHub page "
                                                   "or TrannosRun's itch.io page.")
        os.system('explorer /select,"' + os.path.abspath(os.path.join(thispath, os.pardir)) + '"')
        os.system(r'cmd /c "start /b https://github.com/manydevs/trannosrun/releases/latest"')
        os._exit(0)

else:
    thispath = os.getcwd()
    meipath = thispath

appdatapath = os.getenv('APPDATA') + "\\TrannosRun\\"

if not os.path.isdir(os.getenv('APPDATA') + "\\TrannosRun"):
    os.mkdir(os.getenv('APPDATA') + "\\TrannosRun")

if not os.path.isdir(appdatapath + 's-assets'):
    os.mkdir(appdatapath + 's-assets')

if not os.path.isfile(appdatapath + "bgimg.path"):
    open(appdatapath + "bgimg.path", 'x')
bgi = open(appdatapath + "bgimg.path", 'r').read().strip()

if not os.path.isfile(appdatapath + "soundver.info"):
    with redirect_stdout(open(appdatapath + "soundver.info", 'x')):
        print(0)

if os.path.isfile(appdatapath + "volume.info"):
    trackvol = int(open(appdatapath + "volume.info", "r").read().strip())
else:
    trackvol = 50
    with open(appdatapath + "volume.info", "x") as vol:
        with redirect_stdout(vol):
            print(trackvol)


class TqdmUpTo(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)


class DEVMODE(ctypes.Structure):
    # noinspection PyTypeChecker
    _fields_ = [
        ("dmDeviceName", wintypes.WCHAR * 32),
        ("dmSpecVersion", wintypes.WORD),
        ("dmDriverVersion", wintypes.WORD),
        ("dmSize", wintypes.WORD),
        ("dmDriverExtra", wintypes.WORD),
        ("dmFields", wintypes.DWORD),
        ("dmOrientation", wintypes.SHORT),
        ("dmPaperSize", wintypes.SHORT),
        ("dmPaperLength", wintypes.SHORT),
        ("dmPaperWidth", wintypes.SHORT),
        ("dmScale", wintypes.SHORT),
        ("dmCopies", wintypes.SHORT),
        ("dmDefaultSource", wintypes.SHORT),
        ("dmPrintQuality", wintypes.SHORT),
        ("dmColor", wintypes.SHORT),
        ("dmDuplex", wintypes.SHORT),
        ("dmYResolution", wintypes.SHORT),
        ("dmTTOption", wintypes.SHORT),
        ("dmCollate", wintypes.SHORT),
        ("dmFormName", wintypes.WCHAR * 32),
        ("dmLogPixels", wintypes.WORD),
        ("dmBitsPerPel", wintypes.DWORD),
        ("dmPelsWidth", wintypes.DWORD),
        ("dmPelsHeight", wintypes.DWORD),
        ("dmDisplayFlags", wintypes.DWORD),
        ("dmDisplayFrequency", wintypes.DWORD),
    ]


GetVolumeInformationW = ctypes.WinDLL("Kernel32.dll").GetVolumeInformationW
GetVolumeInformationW.argtypes = [
    ctypes.wintypes.LPCWSTR,
    ctypes.wintypes.LPWSTR, ctypes.c_uint32,
    ctypes.POINTER(ctypes.wintypes.DWORD),
    ctypes.POINTER(ctypes.wintypes.DWORD),
    ctypes.POINTER(ctypes.wintypes.DWORD),
    ctypes.wintypes.LPWSTR, ctypes.c_uint32,
]
GetVolumeInformationW.restype = ctypes.wintypes.BOOL
volume_serial = ctypes.wintypes.DWORD(0)
ishwid = GetVolumeInformationW(os.getenv('SYSTEMDRIVE'), None, 0, ctypes.byref(volume_serial), None, None, None, 0)

if ishwid:
    hwid = "trlb:" + str(uuid.UUID(hex=hashlib.md5(str(volume_serial.value).encode("UTF-8")).hexdigest()))
else:
    hwid = "err"
    showwarning("Could not identify this PC",
                "TrannosRun could not identify your PC in order to communicate with the TrannosRun Leaderboards.")

devmode = DEVMODE()
devmode.dmSize = ctypes.sizeof(DEVMODE)
if ctypes.windll.user32.EnumDisplaySettingsW(None, -1, ctypes.byref(devmode)):
    rf = int(devmode.dmDisplayFrequency)
else:
    rf = 60

nowplaying = "(nothing)"
highscorecoords = appdatapath + "highscore.info"
displayscore = 0
thepath = meipath + "\\assets\\"
loop, volaction, skiptrack, rpcupdate = True, False, False, False

dfstdout = system.stdout
dfstderr = system.stderr

RPC = pypresence.Presence(982695479731191878)
r = redis.Redis(host=,
                port=,
                decode_responses=,
                password=)

gscore, connfail, curver = 0, False, "v1.1.0"
pgame = Tk()
screen_width, screen_height = int(pgame.winfo_screenwidth()), int(pgame.winfo_screenheight())
pgame.update()
pgame.destroy()

if not os.path.isfile(highscorecoords):
    with open(highscorecoords, "x") as f:
        with redirect_stdout(f):
            print(0)


def endgame():
    global loop, pgame
    pgame.quit()
    ctypes.windll.kernel32.FreeConsole()
    loop = False
    try:
        RPC.close()
    except (RuntimeError, AssertionError):
        pass
    os._exit(0)


def showconsole():
    if not ctypes.windll.kernel32.GetConsoleWindow():
        ctypes.windll.kernel32.AllocConsole()
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    if hwnd:
        ctypes.windll.user32.ShowWindow(hwnd, 1)
        os.system("title TrannosRun Console")
        system.stdout = open("CONOUT$", "w")
        system.stderr = open("CONOUT$", "w")
        print("TrannosRun Console Window has been summoned!\n")


def hideconsole():
    global dfstdout, dfstderr
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    if hwnd:
        ctypes.windll.user32.ShowWindow(hwnd, 0)
    system.stdout = dfstdout
    system.stderr = dfstderr


def wincenter(query):
    global screen_width, screen_height
    query.update_idletasks()
    windowsize = tuple(int(_) for _ in query.geometry().split('+')[0].split('x'))
    x = screen_width / 2 - windowsize[0] / 2
    y = screen_height / 2 - windowsize[1] / 2
    query.update()
    query.geometry("+%d+%d" % (x, y))
    # noinspection PyBroadException
    try:
        query.after(10, lambda: query.attributes('-topmost', True))
        query.after(20, lambda: query.attributes('-topmost', False))
        query.after(30, lambda: query.focus_force())
    except TclError:
        pass


# noinspection PyBroadException
try:
    import vlc

    isvlc = True
except Exception:
    try:
        requests.get(r'https://example.com/').text.strip()
        q = askyesno("VLC not found", "The game needs VLC media player to be installed in order to play the songs.\n"
                                      "Do you want to download and install it?")
    except requests.exceptions.ConnectionError:
        q = False
        showwarning("VLC not found", "The game needs VLC media player to be installed in order to play the songs.")
    if q:
        for lsct in requests.get(r"https://get.videolan.org/vlc/last/win64/").text.split('\n'):
            if re.compile(r'<a href="vlc-([0-9]+(\.[0-9]+)+)-win64\.exe">'
                          r'vlc-([0-9]+(\.[0-9]+)+)-win64\.exe</a>', re.IGNORECASE).match(lsct) is not None:
                res = lsct.split("\"")[1]
                break
        try:
            showconsole()
            # noinspection PyUnboundLocalVariable
            with TqdmUpTo(unit='B', unit_scale=True, unit_divisor=1024, miniters=1, desc=res) as t:
                getfile("https://get.videolan.org/vlc/last/win64/" + res,
                        filename=os.path.join(thispath, res), reporthook=t.update_to, data=None)
                t.total = t.n
            print("Installing VLC from " + os.path.join(thispath, res) + '...')
            os.system('"' + os.path.join(thispath, res) + "\" /L=1033 /S & del " + os.path.join(thispath, res))
            import vlc

            isvlc = True
            hideconsole()
        except NameError:
            showwarning("Error", "VLC cannot be found. The game will start normally.")
            isvlc = False
    else:
        isvlc = False


# noinspection PyTypeChecker
def startgame():
    global gscore, pgame, highscorecoords, displayscore, curver, screen_width, screen_height, thepath, bgi, r, ishwid
    global curver, trver, connfail, nowplaying, trackvol, volaction, skiptrack, rpcupdate, hwid, rf, appdatapath

    clock = pygame.time.Clock()
    asprspeed = 400
    playerspeed = 600

    try:
        pgame.destroy()
        pgame.quit()
    except (RuntimeError, TclError):
        pass
    gscore, intg = 0, 0

    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super(Player, self).__init__()
            self.surf = pygame.image.load(thepath + 'mavro_jet.png')
            self.surf.set_colorkey((235, 235, 235))
            self.rect = self.surf.get_rect()

        def update(self, prssdkeys):
            if prssdkeys[K_RSHIFT] or prssdkeys[K_LSHIFT]:
                if prssdkeys[K_w] or prssdkeys[K_UP]:
                    self.rect.y -= asprspeed * dt
                if prssdkeys[K_s] or prssdkeys[K_DOWN]:
                    self.rect.y += asprspeed * dt
                if prssdkeys[K_d] or prssdkeys[K_RIGHT]:
                    self.rect.x += asprspeed * dt
                if prssdkeys[K_a] or prssdkeys[K_LEFT]:
                    self.rect.x -= asprspeed * dt
            else:
                if prssdkeys[K_w] or prssdkeys[K_UP]:
                    self.rect.y -= playerspeed * dt
                if prssdkeys[K_s] or prssdkeys[K_DOWN]:
                    self.rect.y += playerspeed * dt
                if prssdkeys[K_d] or prssdkeys[K_RIGHT]:
                    self.rect.x += playerspeed * dt
                if prssdkeys[K_a] or prssdkeys[K_LEFT]:
                    self.rect.x -= playerspeed * dt

            if self.rect.left <= 0:
                self.rect.left = 0
            if self.rect.right > screen_width:
                self.rect.right = screen_width
            if self.rect.top < 0:
                self.rect.top = 0
            if self.rect.bottom > screen_height:
                self.rect.bottom = screen_height

    class Enemy(pygame.sprite.Sprite):
        def __init__(self):
            super(Enemy, self).__init__()
            self.surf = pygame.image.load(thepath + 'tseoi.png')
            self.surf.set_colorkey((235, 235, 235))
            self.rect = self.surf.get_rect(center=(screen_width, random.randint(1, screen_height)))

        def update(self):
            self.rect.x -= asprspeed * dt
            if self.rect.left < 65:
                self.kill()

    class Cloud(pygame.sprite.Sprite):
        def __init__(self):
            super(Cloud, self).__init__()
            self.surf = pygame.image.load(thepath + 'gani.png')
            self.surf.set_colorkey((225, 0, 0))
            self.rect = self.surf.get_rect(center=(screen_width, random.randint(1, screen_height)))

        def update(self):
            self.rect.x -= asprspeed * dt
            if self.rect.left < 80:
                self.kill()

    pygame.init()

    counter, timer, score = 0, '0'.rjust(3), '0'.rjust(3)
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    font = pygame.font.SysFont('Consolas', 30)
    guncount = int(round((screen_width * screen_height) / 148114))
    if guncount == 0:
        showerror("Low screen resolution", "The screen resolution is too low.\nTrannosRun will now exit.")
        endgame()

    ADDENEMY = pygame.USEREVENT + 1
    CLOUDKILL = pygame.USEREVENT + 2
    UPDATESPEED = pygame.USEREVENT + 3
    interval = 0
    infloop = ""
    cloudkillloop = ""
    cloudupdate = ""
    enemycollide = ""

    for cl in range(guncount):
        globals()["ADDCLOUD" + str(cl)] = pygame.USEREVENT + (4 + cl)
        pygame.time.set_timer(globals()["ADDCLOUD" + str(cl)], 5000 + interval)
        interval += 200
        globals()["cloud" + str(cl)] = Cloud()
        globals()["clouds" + str(cl)] = pygame.sprite.Group()
        infloop += "if event.type == ADDCLOUD" + str(cl) + ":\n\t" \
                                                           "cloud" + str(cl) + " = Cloud()\n\t" \
                                                                               "clouds" + str(cl) + ".add(cloud" + str(
            cl) + ")\n\t" \
                  "all_sprites.add(cloud" + str(cl) + ")\n"
        cloudkillloop += "if pygame.sprite.spritecollideany(player, clouds" + str(cl) + "):\n\t" \
                                                                                        "cloud" + str(
            cl) + ".kill()\n\twhencollected()\n"
        cloudupdate += "cloud" + str(cl) + ".update()\n"
        enemycollide += "if pygame.sprite.spritecollideany(enemy, clouds" + str(cl) + "):\n\t" \
                                                                                      "cloud" + str(cl) + ".kill()\n"

    pygame.time.set_timer(ADDENEMY, 300)
    pygame.time.set_timer(CLOUDKILL, 40)
    pygame.time.set_timer(UPDATESPEED, random.randint(18, 23) * 1000)

    try:
        bg_img = pygame.image.load(bgi)
        bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))
        bgfnd = True
    except (FileNotFoundError, pygame.error):
        bg_img = ""
        bgfnd = False

    screen = pygame.display.set_mode((screen_width, screen_height))

    pygame.display.set_caption('TrannosRun ' + curver.replace("v", ""))
    pygame.display.set_icon(pygame.image.load(thepath + 'mavro_jet.ico'))

    player = Player()
    enemy = Enemy()

    enemies = pygame.sprite.Group()

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    run = True
    pygame.mixer.init()

    def whencollected():
        global gscore, displayscore, rpcupdate
        effect = pygame.mixer.Sound(meipath + "\\assets\\collect.wav")
        effect.set_volume(trackvol / 100)
        effect.play()
        gscore += 1
        displayscore = gscore
        rpcupdate = True

    while run:
        dt = clock.tick(rf) / 1000
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    run = False
                if event.key == K_c:
                    if not trackvol >= 100:
                        trackvol += 10
                        volaction = True
                        with open(appdatapath + "volume.info", "w") as vol:
                            with redirect_stdout(vol):
                                print(trackvol)
                if event.key == K_v:
                    if not trackvol <= 0:
                        trackvol -= 10
                        volaction = True
                        with open(appdatapath + "volume.info", "w") as vol:
                            with redirect_stdout(vol):
                                print(trackvol)
                if event.key == K_g:
                    skiptrack = True
            elif event.type == QUIT:
                run = False

            if event.type == ADDENEMY:
                enemy = Enemy()
                enemies.add(enemy)
                all_sprites.add(enemy)
            exec(infloop.strip())
            if event.type == CLOUDKILL:
                exec(cloudkillloop.strip())
            if event.type == pygame.USEREVENT:
                counter += 1
                timer = str(counter).rjust(3)
            if event.type == UPDATESPEED:
                if asprspeed < 1600 and playerspeed < 1800:
                    asprspeed += 50
                    playerspeed += 50

        prsdkeys = pygame.key.get_pressed()
        player.update(prsdkeys)
        enemies.update()
        exec(cloudupdate.strip())
        screen.fill('#87807E')

        if bgfnd:
            screen.blit(bg_img, (intg, 0))
            screen.blit(bg_img, (screen_width + intg, 0))
            if intg < -1920:
                screen.blit(bg_img, (screen_width + intg, 0))
                intg = 0
            intg -= asprspeed * dt

        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
        if pygame.sprite.spritecollideany(player, enemies):
            player.kill()
            run = False
        exec(enemycollide.strip())

        screen.blit(font.render(timer, True, 'white'), (32, 48))
        score = str(gscore).rjust(3)

        screen.blit(font.render(score, True, 'white'), (screen_width - 132, 48))
        screen.blit(font.render(curver, True, '#00ff00'), (screen_width - 150, screen_height - 50))
        screen.blit(font.render("Volume " + str(trackvol)
                                + "%", True, '#00ffff'), (screen_width - 190, screen_height - 80))
        pygame.display.flip()

    if not run:
        displayscore = '-' + str(gscore) + '-'
        rpcupdate = True

        pygame.quit()
        pgame = Tk()
        pgame.resizable(False, False)
        pgame.title('TrannosRun ' + curver.replace("v", ""))
        pgame.configure(bg='#87807E')
        pgame.iconbitmap(thepath + 'mavro_jet.ico')
        pgame.protocol("WM_DELETE_WINDOW", endgame)

        try:
            ovindex = (gscore / counter) + gscore
        except ZeroDivisionError:
            ovindex = 0

        tempscore = int(open(highscorecoords, 'r').read())
        if 0 == tempscore:
            Label(pgame, text="(Tip: Press Spacebar to play again)", background='#87807E',
                  font=('Consolas', 14, "bold"), foreground='#ffff00').pack()
        if tempscore < gscore:
            endtext = "New high score: " + str(gscore)
            with redirect_stdout(open(highscorecoords, 'w')):
                print(gscore)
        else:
            endtext = "Score: " + str(gscore) + " in " + str(counter) + "sec | Highscore: " + str(tempscore)

        if ishwid:
            def checklb():
                global connfail, curver, trver, hwid
                try:
                    if curver == trver:
                        try:
                            if r.get(hwid) is not None:
                                if float(r.get(hwid).split("¶")[3]) < ovindex:
                                    r.set(hwid, r.get(hwid).split("¶")[0] + "¶" +
                                          str(gscore) + "¶" + str(counter) + "¶" + str(ovindex))
                        except redis.exceptions.ConnectionError:
                            if not connfail:
                                showerror("Timed out", "The Leaderboards service has failed to process your request.\n"
                                                       "All future requests within this session will be halted "
                                                       "unless you restart the game.")
                                connfail = True
                    else:
                        if not connfail:
                            showerror("Connection rejected", "This version of TrannosRun is older than the current "
                                                             "one.\nYour Leaderboards score will not be updated!")
                            connfail = True
                except NameError:
                    pass

            Thread(target=checklb).start()

        wp = Label(pgame, text="Well played!", background='#87807E', font='Consolas 25 bold', foreground='#000000')
        wp.grid(column=0, row=0, sticky=N)

        wp2 = Label(pgame, text=endtext, background='#87807E', font=('Consolas', 12, "bold"), foreground='#000000')
        wp2.grid(column=0, row=1)

        xamenosprep = PhotoImage(file=thepath + 'xamene.png')
        xamenos = Label(pgame, image=xamenosprep, background='#87807E')
        xamenos.grid(column=0, row=3, sticky=N)

        lbl = Label(pgame, text="Now playing: " + nowplaying + " | Volume " + str(trackvol) + "%",
                    background='#87807E', font=('Consolas', 9, "bold"), foreground='#000000')
        lbl.grid(column=0, row=4, sticky=N)

        def helpwin():
            hlp = Toplevel(pgame)
            hlp.title("TrannosRun Controls Dialog")
            hlp.configure(background='#87807E')
            hlp.iconbitmap(thepath + 'mavro_jet.ico')
            hlp.resizable(False, False)

            hlptext1 = """C - Volume up
V - Volume down
G - Skip track
*Esc - Reset
*Shift - Lower speed"""

            hlptext2 = """Same as in-game and:
M - Show track selector
B - Background image selector
Tab - TrannosRun Leaderboards
(not those marked with asterisk)"""

            Label(hlp, background='#87807E', text="In-game:",
                  font=('Consolas', 16, "bold"), foreground='#000000').grid(column=0, row=0, sticky=N)
            Label(hlp, background='#87807E', text=hlptext1,
                  font=('Consolas', 11, "bold"), foreground='#000000').grid(column=0, row=1, sticky=N, padx=20)

            Label(hlp, background='#87807E', text="Death screen:",
                  font=('Consolas', 16, "bold"), foreground='#000000').grid(column=1, row=0, sticky=N)
            Label(hlp, background='#87807E', text=hlptext2,
                  font=('Consolas', 11, "bold"), foreground='#000000').grid(column=1, row=1, sticky=N, padx=20)

            wincenter(hlp)

        btnhelp = Button(pgame, text="Click for controls...", command=helpwin,
                         background='#87807E', font=('Consolas', 9, "bold"), foreground='#000000')
        btnhelp.grid(column=0, row=2, sticky=N, ipadx=127)
        pgame.after(1, lambda: btnhelp.grid(column=0, row=2, sticky=N,
                                            ipadx=pgame.winfo_width() // 2 - 79))

        wincenter(pgame)

        def updatetracks():
            while not run:
                try:
                    pgame.state()
                    temp = [nowplaying, trackvol]
                    sleep(0.05)
                    if temp != [nowplaying, trackvol]:
                        btnhelp.grid_forget()
                        btnhelp.grid(column=0, row=2, sticky=N, ipadx=127)
                        pgame.after(55, lambda: btnhelp.grid(column=0, row=2, sticky=N,
                                                             ipadx=pgame.winfo_width() // 2 - 79))
                        lbl.configure(text="Now playing: " + nowplaying + " | Volume " + str(trackvol) + "%")
                        lbl.update()
                except (TclError, RuntimeError):
                    pass

        Thread(target=updatetracks).start()

        def playonenter(evnt):
            with redirect_stdout(open(os.devnull, "w")):
                print(evnt)
            startgame()
            return "break"

        def tkvolup(evnt):
            global trackvol, volaction, appdatapath
            with redirect_stdout(open(os.devnull, "w")):
                print(evnt)
            if not trackvol >= 100:
                trackvol += 10
                volaction = True
                with open(appdatapath + "volume.info", "w") as vol:
                    with redirect_stdout(vol):
                        print(trackvol)

        def tkvoldown(evnt):
            global trackvol, volaction, appdatapath
            with redirect_stdout(open(os.devnull, "w")):
                print(evnt)
            if not trackvol <= 0:
                trackvol -= 10
                volaction = True
                with open(appdatapath + "volume.info", "w") as vol:
                    with redirect_stdout(vol):
                        print(trackvol)

        def tkskip(evnt):
            global skiptrack
            with redirect_stdout(open(os.devnull, "w")):
                print(evnt)
            skiptrack = True

        def tktooltip(evnt):
            global appdatapath, loop
            with redirect_stdout(open(os.devnull, "w")):
                print(evnt)
            pgame.withdraw()
            loop = False
            gui()

        def tkopenbg(evnt):
            global bgi, appdatapath
            with redirect_stdout(open(os.devnull, "w")):
                print(evnt)
            bgi = askopenfilename(filetypes=[("Images", ".bmp .gif .jpg .jpeg .lbm .pcx .png "
                                                        ".pnm .svg .tga .tif .tiff .webp .xpm")])
            if not bgi == "":
                with redirect_stdout(open(appdatapath + "bgimg.path", 'w', encoding="utf-8")):
                    print(bgi)
                startgame()
            else:
                qi = askyesnocancel("No image selected", "No background image was selected.\n"
                                                         "Do you wish to clear the background image, "
                                                         "keep the old one or reset?\n\n"
                                                         "Yes: Keep\nNo: Reset\nCacnel: Clear")
                if qi is True:
                    bgi = open(appdatapath + "bgimg.path", 'r', encoding="utf-8").read().strip()
                    startgame()
                elif qi is False:
                    bgi = meipath + "assets/bg.jpg"
                    with redirect_stdout(open(appdatapath + "bgimg.path", 'w', encoding="utf-8")):
                        print(bgi)
                    startgame()
                elif qi is None:
                    with redirect_stdout(open(appdatapath + "bgimg.path", 'w', encoding="utf-8")):
                        print(bgi)
                    startgame()

        def tkopenlb(evnt):
            global ishwid
            with redirect_stdout(open(os.devnull, "w")):
                print(evnt)
            if ishwid:
                trlb = Toplevel(pgame)
                trlb.focus_force()
                trlb.resizable(False, False)
                trlb.configure(bg='#87807E')
                trlb.iconbitmap(thepath + 'mavro_jet.ico')
                trlb.title("TrannosRun Leaderboards")

                def hasname(nest):
                    global hwid
                    canuse = False
                    nesteduse = True
                    with redirect_stdout(open(os.devnull, "w")):
                        print(nest)
                    try:
                        with redirect_stdout(open(os.devnull, "w")):
                            print(etr.get()[13])
                        showerror("Try again.", "You have exceeded the 13 character limit!")
                    except IndexError:
                        for char in list(etr.get().strip().lower()):
                            if char not in string.ascii_lowercase + string.digits + '-_':
                                showerror("Try again.", "Illegal character found: " + char)
                                nesteduse = False
                                break
                        if nesteduse:
                            for item in r.keys():
                                if etr.get().strip().lower() == r.get(item).split("¶")[0].lower():
                                    showerror("Try again.", "This user already exists.")
                                    canuse = False
                                    break
                                canuse = True
                        if canuse:
                            r.set(hwid, etr.get().strip() + "¶" + str(gscore) + "¶" + str(counter) + "¶" + str(ovindex))
                            etr.delete(0, END)
                            req.destroy()
                            showinfo("Success!", "Username saved!\nPress Tab to open the Leaderboards.")
                            trlb.destroy()

                def isindb():
                    global hwid
                    try:
                        for cloudid in r.keys():
                            if cloudid == hwid:
                                return False
                        return True
                    except redis.exceptions.ConnectionError:
                        showerror("No internet connection",
                                  "TrannosRun was unable to connect to the Leaderboards service.\n"
                                  "Perhaps the internet connection is unstable or dysfunctional.")

                def ability():
                    (Label(trlb, text="TrannosRun Leaderboards", bg="#87807E", font="Consolas 18 bold")
                     .grid(column=0, row=0, columnspan=3))
                    Label(trlb, text="Username", bg="#87807E", font="Consolas 14 bold").grid(column=0, row=1)
                    Label(trlb, text="Score", bg="#87807E", font="Consolas 14 bold").grid(column=1, row=1)
                    Label(trlb, text="Time", bg="#87807E", font="Consolas 14 bold").grid(column=2, row=1)
                    srtdict = {}
                    try:
                        for entr in r.keys():
                            actetr = r.get(entr)
                            srtdict[float(actetr.split("¶")[3])] = (actetr.split("¶")[0] + "¶" +
                                                                    actetr.split("¶")[1] + "¶" +
                                                                    actetr.split("¶")[2])
                        for ind in range(20):
                            try:
                                Label(trlb, text=srtdict.get(sorted(srtdict, reverse=True)[ind]).split("¶")[0],
                                      bg="#87807E", font="Consolas 12").grid(column=0, row=ind + 2)
                                Label(trlb, text=srtdict.get(sorted(srtdict, reverse=True)[ind]).split("¶")[1],
                                      bg="#87807E", font="Consolas 12").grid(column=1, row=ind + 2)
                                Label(trlb, text=srtdict.get(sorted(srtdict, reverse=True)[ind]).split("¶")[2],
                                      bg="#87807E", font="Consolas 12").grid(column=2, row=ind + 2)
                            except IndexError:
                                break
                            if not run:
                                break
                        waitwin.destroy()
                    except redis.exceptions.ConnectionError:
                        showerror("No internet connection",
                                  "TrannosRun was unable to connect to the Leaderboards service.\n"
                                  "Perhaps the internet connection is unstable or dysfunctional.")
                        waitwin.destroy()
                        trlb.destroy()

                if curver == trver:
                    dbprs = isindb()
                    if dbprs:
                        req = Toplevel(trlb)
                        req.focus_force()
                        req.resizable(False, False)
                        req.title("TRLB Dialog")
                        req.configure(bg='#87807E')
                        req.iconbitmap(thepath + 'mavro_jet.ico')
                        Label(req, text="Input your name:", bg="#87807E", font="Consolas 16").pack()
                        etr = Entry(req, bg="#756f6d", font="Consolas 13")
                        etr.pack()
                        req.bind("<Return>", hasname)
                        req.mainloop()
                    elif dbprs is None:
                        trlb.destroy()
                    else:
                        waitwin = Toplevel(trlb)
                        waitwin.focus_force()
                        waitwin.resizable(False, False)
                        waitwin.title("TRLB Dialog")
                        waitwin.configure(bg='#87807E')
                        waitwin.iconbitmap(thepath + 'mavro_jet.ico')
                        Label(waitwin, text="Please wait...", bg="#87807E", font="Consolas 14").pack()
                        Thread(target=ability).start()
                else:
                    showerror("Connection rejected", "This version of TrannosRun is older than the current one.\n"
                                                     "The Leaderboards window will now close.")
                    trlb.destroy()
            return "break"

        pgame.bind("<space>", playonenter)
        pgame.bind("c", tkvolup)
        pgame.bind("v", tkvoldown)
        pgame.bind("g", tkskip)
        pgame.bind("m", tktooltip)
        pgame.bind("b", tkopenbg)
        pgame.bind("<Tab>", tkopenlb)
        pgame.mainloop()


def music():
    global nowplaying, loop, trackvol, volaction, skiptrack, rpcupdate, isvlc
    if isvlc:
        soundloc = appdatapath + "s-assets"
        playlist = []
        for path in os.listdir(soundloc):
            if os.path.isfile(os.path.join(soundloc, path)) and "#" not in path and ".ogg" in path:
                path2 = path.replace(".ogg", "")
                playlist.append(path2)
        pback = playlist.copy()

        if len(playlist) != 0:
            random.shuffle(playlist)
            nowplaying = playlist[0]
            playlist.pop(0)

            player = vlc.MediaPlayer(appdatapath + "s-assets\\" + nowplaying + ".ogg")
            vlc.libvlc_audio_set_volume(player, trackvol)
            player.play()

            while loop:
                while player.get_state() not in [vlc.State.Ended,
                                                 vlc.State.Stopped] and player.get_state() != vlc.State.Ended:
                    sleep(0.01)
                    if volaction:
                        vlc.libvlc_audio_set_volume(player, trackvol)
                        volaction = False

                    if skiptrack:
                        if len(playlist) == 0:
                            playlist = pback.copy()
                            random.shuffle(playlist)

                        nowplaying = playlist[0]
                        playlist.pop(0)
                        player.stop()
                        player = vlc.MediaPlayer(appdatapath + "s-assets\\" + nowplaying + ".ogg")
                        vlc.libvlc_audio_set_volume(player, trackvol)
                        player.play()
                        rpcupdate = True
                        skiptrack = False

                    if not loop:
                        player.stop()
                if loop:
                    if len(playlist) == 0:
                        playlist = pback.copy()
                        random.shuffle(playlist)

                    nowplaying = playlist[0]
                    playlist.pop(0)
                    player.stop()
                    player = vlc.MediaPlayer(appdatapath + "s-assets\\" + nowplaying + ".ogg")
                    vlc.libvlc_audio_set_volume(player, trackvol)
                    player.play()
                    rpcupdate = True


def discord():
    global displayscore, highscorecoords, curver, nowplaying, loop, rpcupdate, RPC
    try:
        print("Trying to connect...")
        RPC.connect()
        print("Opened")
        epoch = int(time())
        with open(highscorecoords, "r") as f2:
            getlastscore = int(f2.read())
        RPC.update(state="Score: " + str(displayscore) + " | Highscore: " + str(getlastscore),
                   details="Listening to: " + nowplaying,
                   large_image='rpcicon',
                   start=epoch, large_text=curver)
        while True:
            if rpcupdate:
                with open(highscorecoords, "r") as f2:
                    getlastscore = int(f2.read())
                RPC.update(state="Score: " + str(displayscore) + " | Highscore: " + str(getlastscore),
                           details="Listening to: " + nowplaying,
                           large_image='rpcicon',
                           start=epoch, large_text=curver)
                rpcupdate = False
            sleep(0.1)
    except pypresence.exceptions.PyPresenceException:
        pass


tracklinks, tracklist = list(), list()


def gettracks():
    global tracklinks, tracklist

    showconsole()
    temp = requests.get(
        'https://raw.githubusercontent.com/'
        'manydevs/trannosrun/refs/heads/main/soundlib.txt').text.strip().split("\n")
    sv = int(temp[0].strip().replace("TrannosRun Tracklist: version ", ""))
    temp.pop(0)
    tracklinks = []
    tracklist = []

    for tracks in range(len(temp)):
        tracklinks.append(temp[tracks].split("¶")[0])
        if '\r' in temp[tracks]:
            temp[tracks] = temp[tracks].replace('\r', "")
        tracklist.append(temp[tracks].split("¶")[1])

    trackdir = appdatapath + 's-assets'

    print("Downloading tracks to " + trackdir + "...")
    for tracks in range(int(len(tracklist))):
        if not (tracklist[tracks] in os.listdir(trackdir) or '#' + tracklist[tracks] in os.listdir(trackdir)):
            with TqdmUpTo(unit='B', unit_scale=True, unit_divisor=1024, miniters=1,
                          desc=tracklist[tracks].replace('.ogg', "")) as tq:
                getfile(
                    tracklinks[tracks],
                    filename=trackdir + '\\' + tracklist[tracks],
                    reporthook=tq.update_to,
                    data=None
                )
                tq.total = tq.n

    with redirect_stdout(open(appdatapath + "soundver.info", 'w')):
        print(sv)
    hideconsole()
    gui()


def gui():
    global loop, pgame

    selgui = Toplevel(pgame)
    selgui.resizable(False, False)
    frm = Frame(selgui, bg='#87807E')
    frm.pack(fill=BOTH, expand=1)
    cnv = Canvas(frm, bg='#87807E')
    cnv.pack(side=LEFT, fill=BOTH, expand=1)
    scrollbar = Scrollbar(frm, orient=VERTICAL, command=cnv.yview, bg='#87807E')
    scrollbar.pack(side=RIGHT, fill=Y)
    cnv.configure(yscrollcommand=scrollbar.set)
    cnv.bind('<Configure>', lambda e: cnv.configure(scrollregion=cnv.bbox("all")))
    mainframe = Frame(cnv, width=1000, height=100, bg='#87807E')

    selgui.focus_force()
    selgui.configure(bg='#87807E')
    selgui.iconbitmap(meipath + '\\assets\\mavro_jet.ico')
    selgui.title("TrannosRun Launcher")
    soundloc = appdatapath + "s-assets"
    soundfiles = []
    Label(mainframe, text="TrannosRun Track List",
          font="Consolas 21 bold", bg='#87807E').grid(column=0, row=0, columnspan=2)
    Label(mainframe, text="Select the songs you would like to hear while in game.",
          font="Consolas 12 bold", bg='#87807E').grid(column=0, row=1, columnspan=2)
    confb = Button(mainframe, text="Confirm", bg="#87807E", font="Consolas 12 bold")
    confb.grid(column=0, row=2, columnspan=2)
    selb = Button(mainframe, text="Select all", bg="#87807E", font="Consolas 8 bold", width=12)
    selb.grid(column=0, row=2)

    for path in os.listdir(soundloc):
        if os.path.isfile(os.path.join(soundloc, path)) and ".ogg" in path:
            path2 = path.replace(".ogg", "")
            soundfiles.append(path2)

    ii = 3

    for i in soundfiles:
        Label(mainframe, text=i.replace("#", ""), font="Consolas 11", bg='#87807E') \
            .grid(sticky='w', column=1, row=ii)
        globals()["int" + str(ii)] = IntVar(mainframe)
        globals()["ch" + str(ii)] = Checkbutton(mainframe, bg='#87807E', variable=globals()["int" + str(ii)])
        globals()["ch" + str(ii)].grid(column=0, row=ii)
        if "#" not in i:
            globals()["ch" + str(ii)].select()
            selb.configure(text='Deselect all')
            selb.update()
        ii += 1
    ii -= 3

    selgui.after(10, lambda: selgui.geometry(str(mainframe.winfo_width() + 20) + "x650"))
    selgui.after(12, lambda: wincenter(selgui))

    def usl():
        if selb['text'] == "Deselect all":
            for i3 in range(ii):
                globals()["ch" + str(i3 + 3)].deselect()
                selb.configure(text='Select all')
        else:
            for i3 in range(ii):
                globals()["ch" + str(i3 + 3)].select()
                selb.configure(text='Deselect all')

    def yes():
        global loop
        for d in soundfiles:
            if int(globals()["int" + str(soundfiles.index(d) + 3)].get()) == 0 and "#" not in d:
                os.rename(soundloc + "\\" + d + ".ogg", soundloc + "\\#" + d + ".ogg")
            if int(globals()["int" + str(soundfiles.index(d) + 3)].get()) == 1 and "#" in d:
                os.rename(soundloc + "\\" + d + ".ogg", soundloc + "\\" + d.replace("#", "") + ".ogg")
        selgui.destroy()
        selgui.quit()
        loop = True
        Thread(target=music).start()
        startgame()

    selgui.protocol("WM_DELETE_WINDOW", yes)
    selb.configure(command=usl)
    confb.configure(command=yes)
    cnv.create_window((0, 0), window=mainframe, anchor="nw")


try:
    response = requests.get("https://api.github.com/repos/manydevs/trannosrun/releases/latest")
    trver = (response.json()["name"]).replace("TrannosRun ", "")
    if not curver == trver:
        if askyesno("Updates available", "TrannosRun detected it has updates available.\nCurrent version: "
                                         + curver + "\nNew version: " + trver + "\nDo you want to download them?"):
            showconsole()
            with TqdmUpTo(unit='B', unit_scale=True, unit_divisor=1024, miniters=1,
                          desc="trannosrun-v" + trver + ".exe") as t:
                getfile(
                    response.json()["assets"][0]["browser_download_url"],
                    filename=thispath + "\\trannosrun-v" + trver + ".exe",
                    reporthook=t.update_to,
                    data=None
                )
                t.total = t.n
            hideconsole()
            os.system('explorer /select,"' + thispath + '"')
            os._exit(0)
    else:
        soundver = int(requests.get(
            'https://raw.githubusercontent.com/manydevs/trannosrun/refs/heads/main/soundlib.txt')
                       .text.strip().split("\n")[0].strip().replace("TrannosRun Tracklist: version ", ""))
        trackppl = len(requests.get(
            'https://raw.githubusercontent.com/manydevs/trannosrun/refs/heads/main/soundlib.txt')
                       .text.strip().split("\n")) - 1
        if soundver != int(open(appdatapath + "soundver.info", 'r').read().strip()) \
                or trackppl > len(os.listdir(appdatapath + 's-assets')):
            gettracks()
        else:
            Thread(target=music).start()
            Thread(target=discord).start()
            startgame()
except requests.exceptions.ConnectionError:
    Thread(target=music).start()
    Thread(target=discord).start()
    startgame()
except KeyError:
    soundver = int(requests.get(
        'https://raw.githubusercontent.com/manydevs/trannosrun/refs/heads/main/soundlib.txt')
                   .text.strip().split("\n")[0].strip().replace("TrannosRun Tracklist: version ", ""))
    trackppl = len(requests.get(
        'https://raw.githubusercontent.com/manydevs/trannosrun/refs/heads/main/soundlib.txt')
                   .text.strip().split("\n")) - 1
    if soundver != int(open(appdatapath + "soundver.info", 'r').read().strip()) \
            or trackppl > len(os.listdir(appdatapath + 's-assets')):
        gettracks()
    else:
        Thread(target=music).start()
        Thread(target=discord).start()
        startgame()
