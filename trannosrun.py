import random, os, psutil, time, sys
# import cv2
from tkinter import *
from pypresence import Presence
from win32api import GetSystemMetrics
from contextlib import redirect_stdout

with redirect_stdout(open(os.devnull, 'w')):
    import pygame
from pygame.locals import K_w, K_s, K_a, K_d, K_ESCAPE, KEYDOWN, QUIT

if not os.path.exists(os.getenv('APPDATA') + "\\TrannosRun"):
    os.mkdir(os.getenv('APPDATA') + "\\TrannosRun")

highscorecoords = os.getenv('APPDATA') + "\\TrannosRun\\highscore.ak47"
gscore = 0
pgame = Tk()

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
    RPC = Presence(982695479731191878)
    try:
        RPC.connect()
    except:
        exit("Could not connect to Discord RPC Service!")


def startgame():
    global gscore, pgame, highscorecoords
    asprspeed = 5
    playerspeed = 7
    epoch = int(time.time())
    pgame.destroy()
    gscore = 0

    thepath = os.getcwd() + "\\assets\\"
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
                "FY, Light, Trannos - Obsessed"]

    clock = pygame.time.Clock()

    ssel1 = playlist[random.randint(0, len(playlist) - 1)]
    ssel2 = playlist[random.randint(0, len(playlist) - 1)]
    while ssel1 == ssel2:
        ssel2 = playlist[random.randint(0, len(playlist) - 1)]

    pygame.mixer.init()
    mixer = pygame.mixer.Sound(os.getcwd() + "\\s-assets\\" + ssel1 + ".mp3")
    soundmixdelay = int(mixer.get_length()) * 1000
    mixer2 = pygame.mixer.Sound(os.getcwd() + "\\s-assets\\" + ssel2 + ".mp3")
    collectsound = pygame.mixer.Sound(os.getcwd() + "\\s-assets\\collect.mp3")

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
        RPC.update(state="Highscore: " + str(getlastscore),
                   details="Listening to: " + ssel1,
                   large_image='http://cdn.discordapp.com/attachments/832302343268728903/982699191757312000/rpcicon.png',
                   start=epoch)

    mixer.set_volume(0.15)
    mixer2.set_volume(0.15)
    mixer.play()

    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super(Player, self).__init__()
            self.surf = pygame.image.load(thepath + 'mavro_jet.png')
            self.surf.set_colorkey((235, 235, 235))
            self.rect = self.surf.get_rect()

        def update(self, prsdkeys):
            if prsdkeys[K_w]:
                self.rect.move_ip(0, int("-" + str(playerspeed)))
            if prsdkeys[K_s]:
                self.rect.move_ip(0, playerspeed)
            if prsdkeys[K_d]:
                self.rect.move_ip(playerspeed, 0)
            if prsdkeys[K_a]:
                self.rect.move_ip(int("-" + str(playerspeed)), 0)

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
            self.rect.move_ip(int("-" + str(asprspeed)), 0)
            if self.rect.left < 65:
                self.kill()

    class Cloud(pygame.sprite.Sprite):
        def __init__(self):
            super(Cloud, self).__init__()
            self.surf = pygame.image.load(thepath + 'gani.png')
            self.surf.set_colorkey((225, 0, 0))
            self.rect = self.surf.get_rect(center=(screen_width - 20, random.randint(1, screen_height)))

        def update(self):
            self.rect.move_ip(int("-" + str(asprspeed)), 0)
            if self.rect.left < 80:
                self.kill()

    pygame.init()
    SOUNDMIX = pygame.USEREVENT + 11
    pygame.time.set_timer(SOUNDMIX, soundmixdelay)

    counter, timer, score, versionname = 0, '0'.rjust(3), '0'.rjust(3), "v0.8.1"
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    font = pygame.font.SysFont('Consolas', 30)

    ADDENEMY = pygame.USEREVENT + 1
    CLOUDKILL = pygame.USEREVENT + 2
    UPDATESPEED = pygame.USEREVENT + 12
    ADDCLOUD = pygame.USEREVENT + 3
    ADDCLOUD2 = pygame.USEREVENT + 4
    ADDCLOUD3 = pygame.USEREVENT + 5
    ADDCLOUD4 = pygame.USEREVENT + 6
    ADDCLOUD5 = pygame.USEREVENT + 7
    ADDCLOUD6 = pygame.USEREVENT + 8
    ADDCLOUD7 = pygame.USEREVENT + 9
    ADDCLOUD8 = pygame.USEREVENT + 10
    ADDCLOUD9 = pygame.USEREVENT + 13
    ADDCLOUD10 = pygame.USEREVENT + 14
    ADDCLOUD11 = pygame.USEREVENT + 15

    pygame.time.set_timer(ADDENEMY, 300)
    pygame.time.set_timer(ADDCLOUD, 5000)
    pygame.time.set_timer(ADDCLOUD2, 5200)
    pygame.time.set_timer(ADDCLOUD3, 5400)
    pygame.time.set_timer(ADDCLOUD4, 5600)
    pygame.time.set_timer(ADDCLOUD5, 5800)
    pygame.time.set_timer(ADDCLOUD6, 6000)
    pygame.time.set_timer(ADDCLOUD7, 6200)
    pygame.time.set_timer(ADDCLOUD8, 6400)
    pygame.time.set_timer(ADDCLOUD9, 6600)
    pygame.time.set_timer(ADDCLOUD10, 6800)
    pygame.time.set_timer(ADDCLOUD11, 7000)
    pygame.time.set_timer(CLOUDKILL, 40)
    pygame.time.set_timer(UPDATESPEED, 18000)

    screen_width, screen_height = int(GetSystemMetrics(0)), int(GetSystemMetrics(1))
    screen = pygame.display.set_mode((screen_width, screen_height))
    # video = cv2.VideoCapture("bg.mp4")
    # success, video_image = video.read()
    # resized = cv2.resize(video_image, (screen_width, screen_height), interpolation=cv2.INTER_AREA)
    # video_surf = pygame.image.frombuffer(resized.tobytes(), resized.shape[1::-1], "BGR")

    pygame.display.set_caption('TrannosRun')
    pygame.display.set_icon(pygame.image.load(thepath + 'mavro_jet.ico'))

    player = Player()
    enemy = Enemy()
    cloud = Cloud()
    cloud2 = Cloud()
    cloud3 = Cloud()
    cloud4 = Cloud()
    cloud5 = Cloud()
    cloud6 = Cloud()
    cloud7 = Cloud()
    cloud8 = Cloud()
    cloud9 = Cloud()
    cloud10 = Cloud()
    cloud11 = Cloud()

    enemies = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    clouds2 = pygame.sprite.Group()
    clouds3 = pygame.sprite.Group()
    clouds4 = pygame.sprite.Group()
    clouds5 = pygame.sprite.Group()
    clouds6 = pygame.sprite.Group()
    clouds7 = pygame.sprite.Group()
    clouds8 = pygame.sprite.Group()
    clouds9 = pygame.sprite.Group()
    clouds10 = pygame.sprite.Group()
    clouds11 = pygame.sprite.Group()

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    run = True
    localvar = True

    def whencollected():
        global gscore
        collectsound.set_volume(0.05)
        collectsound.play(0)
        gscore += 1

    while run:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    run = False
            elif event.type == QUIT:
                run = False
                pygame.quit()

            if event.type == ADDENEMY:
                enemy = Enemy()
                enemies.add(enemy)
                all_sprites.add(enemy)
            if event.type == ADDCLOUD:
                cloud = Cloud()
                clouds.add(cloud)
                all_sprites.add(cloud)
            if event.type == ADDCLOUD2:
                cloud2 = Cloud()
                clouds2.add(cloud2)
                all_sprites.add(cloud2)
            if event.type == ADDCLOUD3:
                cloud3 = Cloud()
                clouds3.add(cloud3)
                all_sprites.add(cloud3)
            if event.type == ADDCLOUD4:
                cloud4 = Cloud()
                clouds4.add(cloud4)
                all_sprites.add(cloud4)
            if event.type == ADDCLOUD5:
                cloud5 = Cloud()
                clouds5.add(cloud5)
                all_sprites.add(cloud5)
            if event.type == ADDCLOUD6:
                cloud6 = Cloud()
                clouds6.add(cloud6)
                all_sprites.add(cloud6)
            if event.type == ADDCLOUD7:
                cloud7 = Cloud()
                clouds7.add(cloud7)
                all_sprites.add(cloud7)
            if event.type == ADDCLOUD8:
                cloud8 = Cloud()
                clouds8.add(cloud8)
                all_sprites.add(cloud8)
            if event.type == ADDCLOUD9:
                cloud9 = Cloud()
                clouds9.add(cloud9)
                all_sprites.add(cloud9)
            if event.type == ADDCLOUD10:
                cloud10 = Cloud()
                clouds10.add(cloud10)
                all_sprites.add(cloud10)
            if event.type == ADDCLOUD11:
                cloud11 = Cloud()
                clouds11.add(cloud11)
                all_sprites.add(cloud11)
            if event.type == CLOUDKILL:
                if pygame.sprite.spritecollideany(player, clouds):
                    cloud.kill()
                    whencollected()
                if pygame.sprite.spritecollideany(player, clouds2):
                    cloud2.kill()
                    whencollected()
                if pygame.sprite.spritecollideany(player, clouds3):
                    cloud3.kill()
                    whencollected()
                if pygame.sprite.spritecollideany(player, clouds4):
                    cloud4.kill()
                    whencollected()
                if pygame.sprite.spritecollideany(player, clouds5):
                    cloud5.kill()
                    whencollected()
                if pygame.sprite.spritecollideany(player, clouds6):
                    cloud6.kill()
                    whencollected()
                if pygame.sprite.spritecollideany(player, clouds7):
                    cloud7.kill()
                    whencollected()
                if pygame.sprite.spritecollideany(player, clouds8):
                    cloud8.kill()
                    whencollected()
                if pygame.sprite.spritecollideany(player, clouds9):
                    cloud9.kill()
                    whencollected()
                if pygame.sprite.spritecollideany(player, clouds10):
                    cloud10.kill()
                    whencollected()
                if pygame.sprite.spritecollideany(player, clouds11):
                    cloud11.kill()
                    whencollected()
            if event.type == pygame.USEREVENT:
                counter += 1
                timer = str(counter).rjust(3) if counter > 0 else 'Boom!'
            if event.type == SOUNDMIX:
                if localvar:
                    ssel1 = playlist[random.randint(0, len(playlist) - 1)]
                    ssel2 = playlist[random.randint(0, len(playlist) - 1)]
                    while ssel1 == ssel2:
                        ssel2 = playlist[random.randint(0, len(playlist) - 1)]
                    soundmixdelay = int(mixer2.get_length()) * 1000
                    pygame.time.set_timer(SOUNDMIX, soundmixdelay)
                    mixer2.play()
                    mixer.stop()
                    mixer = pygame.mixer.Sound(os.getcwd() + "\\s-assets\\" + ssel1 + ".mp3")
                    mixer.set_volume(0.15)
                    localvar = False
                    if cpr('discord.exe') or cpr('discordptb.exe') or cpr('discordcanary.exe'):
                        RPC.update(state="Highscore: " + str(gscore),
                                   details="Listening to: " + ssel2,
                                   large_image='http://cdn.discordapp.com/attachments/832302343268728903/982699191757312000/rpcicon.png',
                                   start=epoch)
                elif not localvar:
                    ssel1 = playlist[random.randint(0, len(playlist) - 1)]
                    ssel2 = playlist[random.randint(0, len(playlist) - 1)]
                    while ssel1 == ssel2:
                        ssel2 = playlist[random.randint(0, len(playlist) - 1)]
                    soundmixdelay = int(mixer.get_length()) * 1000
                    pygame.time.set_timer(SOUNDMIX, soundmixdelay)
                    mixer.play()
                    mixer2.stop()
                    mixer2 = pygame.mixer.Sound(os.getcwd() + "\\s-assets\\" + ssel2 + ".mp3")
                    mixer2.set_volume(0.15)
                    localvar = True
                    if cpr('discord.exe') or cpr('discordptb.exe') or cpr('discordcanary.exe'):
                        RPC.update(state="Highscore: " + str(gscore),
                                   details="Listening to: " + ssel1,
                                   large_image='http://cdn.discordapp.com/attachments/832302343268728903/982699191757312000/rpcicon.png',
                                   start=epoch)
            if event.type == UPDATESPEED:
                if asprspeed < 40 and playerspeed < 40:
                    asprspeed += 1
                    playerspeed += 1

        prsdkeys = pygame.key.get_pressed()
        player.update(prsdkeys)
        enemies.update()
        clouds.update()
        clouds2.update()
        clouds3.update()
        clouds4.update()
        clouds5.update()
        clouds6.update()
        clouds7.update()
        clouds8.update()
        clouds9.update()
        clouds10.update()
        clouds11.update()

        screen.fill('#87807E')
        # screen.blit(video_surf, (0, 0))

        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)
        if pygame.sprite.spritecollideany(player, enemies):
            player.kill()
            run = False
        if pygame.sprite.spritecollideany(enemy, clouds):
            cloud.kill()
        if pygame.sprite.spritecollideany(enemy, clouds2):
            cloud2.kill()
        if pygame.sprite.spritecollideany(enemy, clouds3):
            cloud3.kill()
        if pygame.sprite.spritecollideany(enemy, clouds4):
            cloud4.kill()
        if pygame.sprite.spritecollideany(enemy, clouds5):
            cloud5.kill()
        if pygame.sprite.spritecollideany(enemy, clouds6):
            cloud6.kill()
        if pygame.sprite.spritecollideany(enemy, clouds7):
            cloud7.kill()
        if pygame.sprite.spritecollideany(enemy, clouds8):
            cloud8.kill()
        if pygame.sprite.spritecollideany(enemy, clouds9):
            cloud9.kill()
        if pygame.sprite.spritecollideany(enemy, clouds10):
            cloud10.kill()
        if pygame.sprite.spritecollideany(enemy, clouds11):
            cloud11.kill()

        screen.blit(font.render(timer, True, ('white')), (32, 48))
        score = str(gscore).rjust(3)
        screen.blit(font.render(score, True, ('white')), (screen_width - 132, 48))
        screen.blit(font.render(versionname, True, ('#00ff00')), (screen_width - 125, screen_height - 50))
        pygame.display.flip()
        clock.tick(72)

    if not run:
        pygame.quit()
        pgame = Tk()
        pgame.focus()
        pgame.resizable(False, False)
        pgame.title('TrannosRun')
        pgame.configure(bg='#87807E')
        pgame.geometry('800x600')
        pgame.iconbitmap(thepath + 'mavro_jet.ico')

        with open(highscorecoords) as f:
            tempscore = int(f.read())
        if tempscore < gscore:
            with open(highscorecoords, 'w') as f:
                with redirect_stdout(f):
                    print(gscore)

        phimage = PhotoImage(file=thepath + 'xamene.png')

        wp = Label(pgame, text='Well played', background='#87807E', font=('Arial 25 bold'), foreground='black')
        wp.place(x=310, y=20)

        xamenos = Label(pgame, image=phimage, background='#87807E', font=('Arial 15 bold'), foreground='black')
        xamenos.place(x=200, y=100)

        def playonenter(event):
            startgame()

        pgame.bind("<Return>", playonenter)

        btn = Button(pgame, text='Play again', background='white', font=('Arial 20 bold'), foreground='black',
                     command=startgame)
        btn.place(x=315, y=500)

        pgame.mainloop()


startgame()
