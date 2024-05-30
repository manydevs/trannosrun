import os
import random
from sys import exit
import urllib.request
from contextlib import redirect_stdout
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import (askyesno, showinfo, askyesnocancel, showerror)
import requests
import pygame
import subprocess
from pygame.locals import K_w, K_s, K_a, K_d, K_c, K_v, K_g, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_ESCAPE, KEYDOWN, QUIT
import redis
import base64
from time import sleep
from threading import Thread

if not os.path.isfile(os.getenv('APPDATA') + "\\TrannosRun\\playback.pass"):
    open(os.getenv('APPDATA') + "\\TrannosRun\\playback.pass", "x")

if not os.path.isfile(os.getenv('APPDATA') + "\\TrannosRun\\currentmusic.info"):
    open(os.getenv('APPDATA') + "\\TrannosRun\\currentmusic.info", "x")

if os.path.isfile(os.getenv('APPDATA') + "\\TrannosRun\\bgimg.path"):
    bgi = open(os.getenv('APPDATA') + "\\TrannosRun\\bgimg.path", 'r').read().strip()
else:
    bgi = "assets/bg.jpg"
    with redirect_stdout(open(os.getenv('APPDATA') + "\\TrannosRun\\bgimg.path", 'x')):
        print(bgi)

if os.path.isfile("setup.exe"):
    os.remove("setup.exe")
if os.path.isfile(os.getenv('APPDATA') + "\\TrannosRun\\score.ak47"):
    os.remove(os.getenv('APPDATA') + "\\TrannosRun\\score.ak47")
if os.path.isfile(os.getenv('APPDATA') + "\\TrannosRun\\volume"):
    os.remove(os.getenv('APPDATA') + "\\TrannosRun\\volume")
if os.path.isfile(os.getenv('APPDATA') + "\\TrannosRun\\currentmusic.ak47"):
    os.remove(os.getenv('APPDATA') + "\\TrannosRun\\currentmusic.ak47")
if os.path.isfile(os.getenv('APPDATA') + "\\TrannosRun\\highscore.ak47"):
    print(open(os.getenv('APPDATA') + "\\TrannosRun\\highscore.ak47", "r").read().strip())
    os.remove(os.getenv('APPDATA') + "\\TrannosRun\\highscore.ak47")

highscorecoords = os.getenv('APPDATA') + "\\TrannosRun\\highscore.info"
scorecoords = os.getenv('APPDATA') + "\\TrannosRun\\score.info"
thepath = os.getcwd() + "\\assets\\"

gscore, connfail, curver = 0, False, "v1.0.1"
pgame = Tk()
screen_width, screen_height = int(pgame.winfo_screenwidth()), int(pgame.winfo_screenheight())


def stopplayback():
    if os.path.isfile(os.getenv('APPDATA') + "\\TrannosRun\\playback.pass"):
        os.remove(os.getenv('APPDATA') + "\\TrannosRun\\playback.pass")
    pgame.destroy()
    exit()


try:
    response = requests.get("https://api.github.com/repos/manydevs/trannosrun/releases/latest")
    trver = (response.json()["name"]).replace("TrannosRun ", "")
    if not curver == trver:
        pgame.title("TrannosRun: Pre-Loading Phase")
        Label(pgame, text="A message box is interrupting TrannosRun's initialization. Interact with it to continue.",
              font=("Arial", 8)).pack()
        pgame.iconbitmap(thepath + 'mavro_jet.ico')
        if askyesno("Updates available", "TrannosRun detected it has updates available.\nCurrent version: "
                                         + curver + "\nNew version: " + trver + "\nDo you want to download them?"):
            if os.path.isfile(os.getenv('APPDATA') + "\\TrannosRun\\playback.pass"):
                os.remove(os.getenv('APPDATA') + "\\TrannosRun\\playback.pass")
            pgame.destroy()
            showinfo("Connection established", 'The requested version "' + trver +
                     '" will start downloading and will run after closing this info box. Note that it may take some '
                     'time for the installer to download. Thanks for playing TrannosRun!')
            urllib.request.urlretrieve(response.json()["assets"][0]["browser_download_url"], "setup.exe")
            os.system('start cmd /c "echo '
                      '--- ManyDevs\' TrannosRun Setup Launcher --- '
                      '& color 0a '
                      '& echo The installer will start shortly and this window should close itself. '
                      '& start /b ' + os.getcwd() + '\\setup.exe & taskkill /f /im SilentCMD.exe & exit')
            stopplayback()
except requests.exceptions.ConnectionError:
    pass


# noinspection PyTypeChecker
def startgame():
    global gscore, pgame, highscorecoords, scorecoords, curver, screen_width, screen_height, thepath, bgi
    global curver, trver, connfail
    clock = pygame.time.Clock()
    asprspeed = 7
    playerspeed = 9
    pgame.destroy()
    gscore, intg = 0, 0

    if not os.path.isfile(highscorecoords):
        open(highscorecoords, "x")
        with open(highscorecoords, 'w') as f:
            with redirect_stdout(f):
                print(0)

    if not os.path.isfile(scorecoords):
        open(scorecoords, "x")
    with open(scorecoords, 'w') as f:
        with redirect_stdout(f):
            print(0)

    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super(Player, self).__init__()
            self.surf = pygame.image.load(thepath + 'mavro_jet.png')
            self.surf.set_colorkey((235, 235, 235))
            self.rect = self.surf.get_rect()

        def update(self, prssdkeys):
            if prssdkeys[K_w] or prssdkeys[K_UP]:
                self.rect.move_ip(0, playerspeed * -1)
            if prssdkeys[K_s] or prssdkeys[K_DOWN]:
                self.rect.move_ip(0, playerspeed)
            if prssdkeys[K_d] or prssdkeys[K_RIGHT]:
                self.rect.move_ip(playerspeed, 0)
            if prssdkeys[K_a] or prssdkeys[K_LEFT]:
                self.rect.move_ip(playerspeed * -1, 0)

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
            self.rect = self.surf.get_rect(center=(screen_width - 20, random.randint(1, screen_height)))

        def update(self):
            self.rect.move_ip(asprspeed * -1, 0)
            if self.rect.left < 65:
                self.kill()

    class Cloud(pygame.sprite.Sprite):
        def __init__(self):
            super(Cloud, self).__init__()
            self.surf = pygame.image.load(thepath + 'gani.png')
            self.surf.set_colorkey((225, 0, 0))
            self.rect = self.surf.get_rect(center=(screen_width - 20, random.randint(1, screen_height)))

        def update(self):
            self.rect.move_ip(asprspeed * -1, 0)
            if self.rect.left < 80:
                self.kill()

    pygame.init()

    counter, timer, score = 0, '0'.rjust(3), '0'.rjust(3)
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    font = pygame.font.SysFont('Consolas', 30)
    guncount = int(round((screen_width * screen_height) / 148114))
    if guncount == 0:
        showerror("Low screen resolution", "The screen resolution is too low.\nTrannosRun will now exit.")
        stopplayback()

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
                   "clouds" + str(cl) + ".add(cloud" + str(cl) + ")\n\t" \
                   "all_sprites.add(cloud" + str(cl) + ")\n"
        cloudkillloop += "if pygame.sprite.spritecollideany(player, clouds" + str(cl) + "):\n\t" \
                         "cloud" + str(cl) + ".kill()\n\twhencollected()\n"
        cloudupdate += "cloud" + str(cl) + ".update()\n"
        enemycollide += "if pygame.sprite.spritecollideany(enemy, clouds" + str(cl) + "):\n\t" \
                        "cloud" + str(cl) + ".kill()\n"
    print(enemycollide)

    pygame.time.set_timer(ADDENEMY, 300)
    pygame.time.set_timer(CLOUDKILL, 40)
    pygame.time.set_timer(UPDATESPEED, 18000)

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
        global gscore
        pygame.mixer.Sound("collect.wav").play()
        gscore += 1
        with open(scorecoords, 'w') as scrrd:
            with redirect_stdout(scrrd):
                print(gscore)

    while run:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    run = False
                if event.key == K_c:
                    if not os.path.isfile(os.getenv('APPDATA') + "\\TrannosRun\\volup.pass"):
                        open(os.getenv('APPDATA') + "\\TrannosRun\\volup.pass", "x")
                if event.key == K_v:
                    if not os.path.isfile(os.getenv('APPDATA') + "\\TrannosRun\\voldown.pass"):
                        open(os.getenv('APPDATA') + "\\TrannosRun\\voldown.pass", "x")
                if event.key == K_g:
                    if not os.path.isfile(os.getenv('APPDATA') + "\\TrannosRun\\skiptrack.pass"):
                        open(os.getenv('APPDATA') + "\\TrannosRun\\skiptrack.pass", "x")
            elif event.type == QUIT:
                stopplayback()
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
                if asprspeed < 40 and playerspeed < 40:
                    asprspeed += 1
                    playerspeed += 1

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
            intg -= asprspeed

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
        screen.blit(font.render("Volume " + open(os.getenv('APPDATA') + "\\TrannosRun\\volume.info").read().strip()
                                + "%", True, '#00ffff'), (screen_width - 190, screen_height - 80))
        pygame.display.flip()
        clock.tick(60)

    if not run:
        with open(scorecoords, 'w') as f2:
            with redirect_stdout(f2):
                print('-' + str(gscore) + '-')

        def center(query):
            global screen_width, screen_height
            query.update_idletasks()
            windowsize = tuple(int(_) for _ in query.geometry().split('+')[0].split('x'))
            x = screen_width / 2 - windowsize[0] / 2
            y = screen_height / 2 - windowsize[1] / 2
            query.geometry("+%d+%d" % (-150 + x, -150 + y))

        pygame.quit()
        pgame = Tk()
        center(pgame)
        pgame.focus_force()
        pgame.resizable(False, False)
        pgame.title('TrannosRun ' + curver.replace("v", ""))
        pgame.configure(bg='#87807E')
        pgame.iconbitmap(thepath + 'mavro_jet.ico')
        pgame.protocol("WM_DELETE_WINDOW", stopplayback)

        hwid = "trlb:" + subprocess.check_output('wmic csproduct get uuid').split(b'\n')[1].strip().decode()
        r = redis.Redis(host=,
                        port=,
                        decode_responses=True,
                        password=)

        try:
            ovindex = (gscore / counter) + gscore
        except ZeroDivisionError:
            ovindex = 0

        with open(highscorecoords) as f:
            tempscore = int(f.read())
        if 0 == tempscore:
            Label(pgame, text="(Tip: Press Spacebar to play again)", background='#87807E',
                  font=('Consolas', 14, "bold"), foreground='#ffff00').pack()
        if tempscore < gscore:
            endtext = "New high score: " + str(gscore)
            with open(highscorecoords, 'w') as f:
                with redirect_stdout(f):
                    print(gscore)
        else:
            endtext = "Score: " + str(gscore) + " in " + str(counter) + "sec | Highscore: " + str(tempscore)

        def checklb():
            global connfail, curver, trver
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
                    showerror("Connection rejected", "This version of TrannosRun is older than the current one.\n"
                                                     "Your Leaderboards score will not be updated!")
                    connfail = True

        Thread(target=checklb).start()

        wp = Label(pgame, text="Well played!", background='#87807E', font='Consolas 25 bold', foreground='#000000')
        wp.pack()

        wp2 = Label(pgame, text=endtext, background='#87807E', font=('Consolas', 12, "bold"), foreground='#000000')
        wp2.pack()

        xamenosprep = PhotoImage(file=thepath + 'xamene.png')
        xamenos = Label(pgame, image=xamenosprep, background='#87807E')
        xamenos.pack()

        lbl = Label(pgame, text="Now playing: " +
                                open(os.getenv('APPDATA') + "\\TrannosRun\\currentmusic.info").read().strip() +
                                " | Volume " + open(os.getenv('APPDATA') + "\\TrannosRun\\volume.info").read().strip() +
                                "%",
                    background='#87807E', font=('Consolas', 9, "bold"), foreground='#000000')
        lbl.pack()

        def updatetracks():
            while os.path.isfile(os.getenv('APPDATA') + "\\TrannosRun\\playback.pass"):
                try:
                    pgame.state()
                    trackhandler = open(os.getenv('APPDATA') + "\\TrannosRun\\currentmusic.info").read().strip()
                    volhandler = open(os.getenv('APPDATA') + "\\TrannosRun\\currentmusic.info").read().strip()
                    sleep(0.2)
                    if not trackhandler == open(os.getenv('APPDATA') +
                                                "\\TrannosRun\\currentmusic.info").read().strip() or \
                            volhandler == open(os.getenv('APPDATA') + "\\TrannosRun\\currentmusic.info").read().strip():
                        lbl.configure(text="Now playing: " + open(os.getenv('APPDATA') +
                                                                  "\\TrannosRun\\currentmusic.info").read().strip() +
                                           " | Volume " + open(os.getenv('APPDATA') +
                                                               "\\TrannosRun\\volume.info").read().strip() + "%")
                        lbl.update()
                except TclError:
                    pass
            return

        Thread(target=updatetracks).start()

        def playonenter(evnt):
            with redirect_stdout(open(os.devnull, "w")):
                print(evnt)
            startgame()

        def tkvolup(evnt):
            with redirect_stdout(open(os.devnull, "w")):
                print(evnt)
            if not os.path.isfile(os.getenv('APPDATA') + "\\TrannosRun\\volup.pass"):
                open(os.getenv('APPDATA') + "\\TrannosRun\\volup.pass", "x")

        def tkvoldown(evnt):
            with redirect_stdout(open(os.devnull, "w")):
                print(evnt)
            if not os.path.isfile(os.getenv('APPDATA') + "\\TrannosRun\\voldown.pass"):
                open(os.getenv('APPDATA') + "\\TrannosRun\\voldown.pass", "x")

        def tkskip(evnt):
            with redirect_stdout(open(os.devnull, "w")):
                print(evnt)
            if not os.path.isfile(os.getenv('APPDATA') + "\\TrannosRun\\skiptrack.pass"):
                open(os.getenv('APPDATA') + "\\TrannosRun\\skiptrack.pass", "x")

        def tktooltip(evnt):
            with redirect_stdout(open(os.devnull, "w")):
                print(evnt)
            if os.path.isfile(os.getenv('APPDATA') + "\\TrannosRun\\showplaylist.pass"):
                os.remove(os.getenv('APPDATA') + "\\TrannosRun\\showplaylist.pass")
                showinfo("Restrictions lifted", "Restart the game for the TrannosRun Launcher to show up.")

        def tkopenbg(evnt):
            global bgi
            with redirect_stdout(open(os.devnull, "w")):
                print(evnt)
            bgi = askopenfilename(filetypes=[("Images", ".bmp .gif .jpg .jpeg .lbm .pcx .png "
                                                        ".pnm .svg .tga .tif .tiff .webp .xpm")])
            if not bgi == "":
                with redirect_stdout(open(os.getenv('APPDATA') + "\\TrannosRun\\bgimg.path", 'w')):
                    print(bgi)
                startgame()
            else:
                qi = askyesnocancel("No image selected", "No background image was selected.\n"
                                                         "Do you wish to clear the background image, "
                                                         "keep the old one or reset?\n\n"
                                                         "Yes: Keep\nNo: Reset\nCacnel: Clear")
                if qi is True:
                    bgi = open(os.getenv('APPDATA') + "\\TrannosRun\\bgimg.path", 'r').read().strip()
                    startgame()
                elif qi is False:
                    bgi = "assets/bg.jpg"
                    with redirect_stdout(open(os.getenv('APPDATA') + "\\TrannosRun\\bgimg.path", 'w')):
                        print(bgi)
                    startgame()
                elif qi is None:
                    with redirect_stdout(open(os.getenv('APPDATA') + "\\TrannosRun\\bgimg.path", 'w')):
                        print(bgi)
                    startgame()

        def tkopenlb(evnt):
            with redirect_stdout(open(os.devnull, "w")):
                print(evnt)
            trlb = Toplevel(pgame)
            trlb.focus_force()
            trlb.resizable(False, False)
            trlb.configure(bg='#87807E')
            trlb.iconbitmap(thepath + 'mavro_jet.ico')
            trlb.title("TrannosRun Leaderboards")

            def hasname(nest):
                canuse = False
                with redirect_stdout(open(os.devnull, "w")):
                    print(nest)
                try:
                    with redirect_stdout(open(os.devnull, "w")):
                        print(etr.get()[20])
                    showerror("Try again.", "You have exceeded the 20 character limit!")
                except IndexError:
                    for item in r.keys():
                        if etr.get().strip() == item.split("¶")[0]:
                            showerror("Try again.", "This user already exists.")
                            canuse = False
                            break
                        elif "¶" in etr.get().strip() or " " in etr.get().strip():
                            showerror("Try again.", "You have used a banned character.")
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
                try:
                    for cloudid in r.keys():
                        if cloudid == hwid:
                            return False
                        else:
                            pass
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

        pgame.bind("<space>", playonenter)
        pgame.bind("c", tkvolup)
        pgame.bind("v", tkvoldown)
        pgame.bind("g", tkskip)
        pgame.bind("m", tktooltip)
        pgame.bind("b", tkopenbg)
        pgame.bind("<Tab>", tkopenlb)
        pgame.mainloop()


startgame()
