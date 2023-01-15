import pygame
import sqlite3
import random
import sys
ZOOMconst = 3
screen_rect = (0, 0, 900, 800)


class Hub():
    def __init__(self):
        self.startScreen()
        fade = pygame.Surface((960, 480))
        fade.fill((0, 0, 0))
        clock = pygame.time.Clock()
        background = pygame.image.load("Cheshuya/Sprites/Hub.jpg")
        back = pygame.sprite.Sprite()
        back.image = background
        back.rect = back.image.get_rect()
        back.rect.x = 0
        back.rect.y = 0
        all_sprites.add(back)
        dinoImage = pygame.image.load("Cheshuya/Sprites/DinoSprites - mort.png")
        coords = [(40, 200), (200, 300), (800, 200)]
        dino = Dino(dinoImage, 24, 1, 480, 300, self)
        self.end = EndGame(650, 250, dino)
        all_sprites.add(self.end)
        all_sprites.add(dino)
        all_sprites.update()
        con = sqlite3.connect("Cheshuya/PlayersData.db")
        cur = con.cursor()
        level = cur.execute(f"""SELECT current FROM Player""").fetchall()[0][0]
        con.close()
        if level < 4:
            for i in range(3):
                stone = Stone(coords[i][0], coords[i][1], i + 1, dino)
                stone_sprites.add(stone)
        else:
            for i in range(3):
                stone = BrokenStone(coords[i][0], coords[i][1] + 40)
                brokenStones.add(stone)
        stone_sprites.update()
        all_sprites.draw(screen)
        stone_sprites.draw(screen)
        screen2 = screen.copy()
        for a in range(300, 0, -1):
            screen1 = screen2.copy()
            fade.set_alpha(a)
            screen1.blit(fade, (0, 0))
            screen.blit(screen1, (0, 0))
            pygame.display.update()
            pygame.time.delay(5)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            screen.fill((0, 0, 0))
            all_sprites.draw(screen)
            all_sprites.update()
            stone_sprites.draw(screen)
            stone_sprites.update()
            brokenStones.draw(screen)
            brokenStones.update()
            pygame.display.flip()
            clock.tick(10)
        self.endScreen()
        pygame.quit()

    def startScreen(self):
        backgroundFirst = pygame.image.load("Cheshuya/Sprites/cave.jpg")
        back = pygame.sprite.Sprite()
        back.image = backgroundFirst
        back.rect = back.image.get_rect()
        back.rect.x = 0
        back.rect.y = 0
        all_sprites.add(back)
        press_space = pygame.image.load("Cheshuya/Sprites/press_space.png")
        space = pygame.sprite.Sprite()
        space.image = press_space
        space.rect = back.image.get_rect()
        space.rect.x = 280
        space.rect.y = 300
        start_game = pygame.image.load("Cheshuya/Sprites/start_game.png")
        start = pygame.sprite.Sprite()
        start.image = start_game
        start.rect = back.image.get_rect()
        start.rect.x = 250
        start.rect.y = 150
        all_sprites.add(space)
        all_sprites.add(start)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        running = False
            all_sprites.draw(screen)
            all_sprites.update()
            pygame.display.flip()
        screen2 = screen.copy()
        fade = pygame.Surface((960, 480))
        fade.fill((0, 0, 0))
        for a in range(0, 300):
            screen1 = screen2.copy()
            fade.set_alpha(a)
            screen1.blit(fade, (0, 0))
            screen.blit(screen1, (0, 0))
            pygame.display.update()
            pygame.time.delay(5)
        screen.fill((0, 0, 0))
        all_sprites.remove(space)
        all_sprites.remove(back)
        all_sprites.remove(start)

    def endScreen(self):
        con = sqlite3.connect("Cheshuya/PlayersData.db")
        cur = con.cursor()
        cur.execute("""UPDATE Player
                        SET current = 1""")
        cur.execute("""UPDATE Player
                        SET score = 0""")
        con.commit()
        backgroundFirst = pygame.image.load("Cheshuya/Sprites/cave.jpg")
        back = pygame.sprite.Sprite()
        back.image = backgroundFirst
        back.rect = back.image.get_rect()
        back.rect.x = 0
        back.rect.y = 0
        all_sprites.add(back)
        thankyou = pygame.image.load("Cheshuya/Sprites/thanks.png")
        thank = pygame.sprite.Sprite()
        thank.image = thankyou
        thank.rect = back.image.get_rect()
        thank.rect.x = 250
        thank.rect.y = 100
        cr = pygame.image.load("Cheshuya/Sprites/Creators.png")
        creators = pygame.sprite.Sprite()
        creators.image = cr
        creators.rect = back.image.get_rect()
        creators.rect.x = 250
        creators.rect.y = 500
        all_sprites.add(creators)
        all_sprites.add(thank)
        running = True
        clock = pygame.time.Clock()
        while running:
            if not creators.rect.y != 100:
                creators.rect = creators.rect.move(0, -1)
            thank.rect = thank.rect.move(0, -1)
            clock.tick(50)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        running = False
            all_sprites.draw(screen)
            all_sprites.update()
            pygame.display.flip()
        screen2 = screen.copy()
        fade = pygame.Surface((960, 480))
        fade.fill((0, 0, 0))
        for a in range(0, 300):
            screen1 = screen2.copy()
            fade.set_alpha(a)
            screen1.blit(fade, (0, 0))
            screen.blit(screen1, (0, 0))
            pygame.display.update()
        pygame.time.delay(5)
        screen.fill((0, 0, 0))
        all_sprites.remove(back)
        pygame.quit()
        sys.exit()

    def nowhereToEnter(self):
        self.end.enter = True
        for sprite in stone_sprites:
            stone_sprites.remove(sprite)
            brokenStone = BrokenStone(sprite.x, sprite.y + 40)
            brokenStones.add(brokenStone)


class Dino(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, hub):
        super().__init__(all_sprites)
        self.clock = pygame.time.Clock()
        self.framesRun = []
        self.framesRunLeft = []
        self.framesIdle = []
        self.framesIdleLeft = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.framesIdle[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.face = 'right'
        self.last = 'idle'
        self.hub = hub

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                if i <= 3:
                    frame_location = (self.rect.w * i, self.rect.h * j)
                    self.framesIdle.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))
                elif i <= 9:
                    frame_location = (self.rect.w * i, self.rect.h * j)
                    self.framesRun.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))
        for image in self.framesIdle:
            self.framesIdleLeft.append(pygame.transform.flip(image, True, False))
        for image in self.framesRun:
            self.framesRunLeft.append(pygame.transform.flip(image, True, False))

    def update(self):
        keys = pygame.key.get_pressed()
        idle = True
        if keys[pygame.K_RETURN]:
            a = self.checkCollide()
            if a == 'end_game':
                self.hub.endScreen()
            if a:
                level = Level(a)
                level_sprites.empty()
                screen = pygame.display.set_mode((960, 480))
                if level.end:
                    self.hub.nowhereToEnter()
        if keys[pygame.K_a]:
            self.move(-20, 0)
            self.face = 'left'
            idle = False
        elif keys[pygame.K_d]:
            self.move(20, 0)
            self.face = 'right'
            idle = False
        if keys[pygame.K_w]:
            self.move(0, -20)
            idle = False
        elif keys[pygame.K_s]:
            self.move(0, 20)
            idle = False
        if (self.last == 'idle' and idle) or (self.last == 'run' and not(idle)):
            if self.last == 'idle':
                self.cur_frame = (self.cur_frame + 1) % len(self.framesIdle)
                if self.face == 'left':
                    self.image = self.framesIdleLeft[self.cur_frame]
                else:
                    self.image = self.framesIdle[self.cur_frame]
            else:
                self.cur_frame = (self.cur_frame + 1) % len(self.framesRun)
                if self.face == 'left':
                    self.image = self.framesRunLeft[self.cur_frame]
                else:
                    self.image = self.framesRun[self.cur_frame]
        else:
            self.cur_frame = 0
            if self.last == 'idle':
                self.last = 'run'
                if self.face == 'left':
                    self.image = self.framesIdleLeft[self.cur_frame]
                else:
                    self.image = self.framesIdle[self.cur_frame]
            else:
                self.last = 'idle'
                if self.face == 'left':
                    self.image = self.framesRunLeft[self.cur_frame]
                else:
                    self.image = self.framesRun[self.cur_frame]
        self.image = pygame.transform.scale(self.image, (100, 100))

    def move(self, x, y):
        self.rect = self.rect.move(x, y)

    def checkCollide(self):
        a = pygame.sprite.collide_mask(self, self.hub.end)
        if a:
            return 'end_game'
        for sprite in stone_sprites:
            a = pygame.sprite.collide_mask(self, sprite)
            if a:
                return sprite.hard
        return False


class Stone(pygame.sprite.Sprite):  # камень с рунами
    def __init__(self, x, y, setting, dino):
        super().__init__(stone_sprites)
        self.image = pygame.image.load("Cheshuya/Sprites/stone.png")
        self.x, self.y = x, y
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)
        self.dino = dino
        self.hard = setting
        self.settings = {1: ('Cheshuya/Sprites/easy.png', 0),
                        2: ('Cheshuya/Sprites/medium.png', -20),
                        3:  ('Cheshuya/Sprites/hard.png', 0)}

    def update(self):
        enter_sprites.empty()
        a = pygame.sprite.collide_mask(self, self.dino)
        if a:
            enter = pygame.sprite.Sprite()
            enter.image = pygame.image.load(self.settings[self.hard][0])
            enter.rect = enter.image.get_rect()
            enter.rect.x = self.x + self.settings[self.hard][1]
            enter.rect.y = self.y - 50
            enter_sprites.add(enter)
            enter_sprites.update()
            enter_sprites.draw(screen)


class BrokenStone(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(brokenStones)
        self.image = pygame.image.load("Cheshuya/Sprites/BrokenStone.png")
        self.x, self.y = x, y
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)


class EndGame(pygame.sprite.Sprite):
    def __init__(self, x, y, dino):
        super().__init__(all_sprites)
        self.image = pygame.image.load("Cheshuya/Sprites/Shop.png")
        self.x, self.y = x, y
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)
        self.dino = dino
        self.enter = False

    def update(self):
        if self.enter:
            enter_sprites.empty()
            a = pygame.sprite.collide_mask(self, self.dino)
            if a:
                enter = pygame.sprite.Sprite()
                enter.image = pygame.image.load('Cheshuya/Sprites/enter.png')
                enter.rect = enter.image.get_rect()
                enter.rect.x = self.x
                enter.rect.y = self.y - 50
                enter_sprites.add(enter)
                enter_sprites.update()
                enter_sprites.draw(screen)


class Level():  # уровень
    def __init__(self, hard):
        self.end = False
        current = 0
        screen = pygame.display.set_mode((900, 800))
        con = sqlite3.connect("Cheshuya/PlayersData.db")
        cur = con.cursor()
        result = cur.execute(f"""SELECT * FROM Player""").fetchall()
        con.close()
        level, score = result[0][1], result[0][0]
        background = pygame.image.load(f"Cheshuya/Levels/level{level}.jpg")
        back = pygame.sprite.Sprite()
        back.image = background
        back.rect = back.image.get_rect()
        back.rect.x = 0
        back.rect.y = 0
        need_images = []
        for i in range(1, 6):
            need_images.append(f"Cheshuya/Levels/level{level}.{i}.png")
        f = open(f'Cheshuya/Levels/hitboxes{level}.txt', mode='rt', encoding='utf-8')
        hitboxes = eval(f.readlines()[0])
        f.close()
        need = pygame.sprite.Sprite()
        need.image = pygame.image.load(need_images[0])
        need.rect = need.image.get_rect()
        need.rect.x = 0
        need.rect.y = 550
        screen2  = pygame.Surface((900, 800))
        hit = pygame.sprite.Group()
        hitbox = pygame.sprite.Sprite()
        hitbox.image = pygame.image.load(need_images[0])
        hitbox.rect = hitboxes[0]
        hit.add(hitbox)
        hearts_sprites = pygame.sprite.Group()
        hearts = []
        arrow = pygame.sprite.Sprite()
        arrow.image = pygame.image.load('Cheshuya/Sprites/arrow.png')
        arrow.rect = arrow.image.get_rect()
        level_sprites.add(back)
        level_sprites.add(need)
        level_sprites.add(arrow)
        clock = pygame.time.Clock()
        if hard == 1:
            counter = 120
            hearts_count = 3
        elif hard == 2:
            counter = 90
            hearts_count = 2
        elif hard == 3:
            counter = 60
            hearts_count = 1
        for i in range(hearts_count):
            heartImg = pygame.image.load("Cheshuya/Sprites/Heart.png")
            heart = pygame.sprite.Sprite()
            heart.image = heartImg
            heart.rect = heart.image.get_rect()
            heart.rect.x = 800
            heart.rect.y = 100 * i
            hearts_sprites.add(heart)
            hearts.append(heart)
        text = str(counter)
        pygame.time.set_timer(pygame.USEREVENT, 1000)
        font = pygame.font.SysFont('Consolas', 100)
        running = True
        zoom1 = False
        xMouse = 0
        yMouse = 0
        res = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT:
                    counter -= 1
                    if counter > 0:
                        text = str(counter)
                    else:
                        res = 'lose'
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 3:
                        if zoom1:
                            zoom1 = False
                        else:
                            zoom1 = True
                    elif event.button == 1:
                        x, y = arrow.rect.x, arrow.rect.y
                        a = pygame.sprite.collide_mask(arrow, hitbox)
                        if a:
                            create_particles((x, y), True)
                            current += 1
                            if current == len(need_images):
                                res = 'win'
                            else:
                                need.image = pygame.image.load(need_images[current])
                                hitbox.image = pygame.image.load(need_images[current])
                                hitbox.rect = hitboxes[current]
                        else:
                            create_particles((x, y), False)
                            hearts_sprites.remove(hearts[-1])
                            del hearts[-1]
                            if len(hearts) == 0:
                                res = 'lose'
            if res:
                break
            if pygame.mouse.get_focused():
                x, y = pygame.mouse.get_pos()
                arrow.rect.x = x
                arrow.rect.y = y
            screen.fill((0, 0, 0))
            hearts_sprites.draw(screen)
            hearts_sprites.update()
            level_sprites.draw(screen)
            level_sprites.update()
            screen.blit(font.render(text, True, (255, 255, 255)), (700, 600))
            hit.draw(screen2)
            screen2.set_alpha(0)
            screen.blit(screen2, (0, 0))
            if zoom1 and xMouse != 0 and yMouse != 0:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_a]:
                    xMouse -= 5
                elif keys[pygame.K_d]:
                    xMouse += 5
                elif keys[pygame.K_w]:
                    yMouse -= 5
                elif keys[pygame.K_s]:
                    yMouse += 5
            if zoom1:
                zoom = ZOOMconst
                width, height = screen.get_size()
                zoom_size = (round(width / zoom), round(height / zoom))
                zoom_area = pygame.Rect(0, 0, zoom_size[0], zoom_size[1])
                if xMouse == yMouse == 0:
                    xMouse, yMouse = pygame.mouse.get_pos()
                zoom_area.center = (xMouse, yMouse)
                zoom_surf = pygame.Surface(zoom_area.size)
                zoom_surf.blit(screen, (0, 0), zoom_area)
                zoom_surf = pygame.transform.smoothscale(zoom_surf, (width, height))
                screen.blit(zoom_surf, (0, 0))
            else:
                xMouse = 0
                yMouse = 0
            pygame.display.flip()
            clock.tick(60)
        con = sqlite3.connect("Cheshuya/PlayersData.db")
        cur = con.cursor()
        if res == 'win':
            plusScore = hard * 10
            cur.execute(f"""UPDATE Player
                            SET current = current + 1""")
            cur.execute(f"""UPDATE Player
                            SET score = score + {plusScore}""")
            if level == 3:
                self.end = True
        else:
            plusScore = hard * 15
            cur.execute(f"""UPDATE Player
                            SET score = score - {plusScore}""")
        con.commit()
        con.close()


class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, condition, dx=random.choice(range(-6, 5)), dy=random.choice(range(-6, 5))):
        super().__init__(level_sprites)
        if condition:
            self.fire = [pygame.image.load("Cheshuya/Sprites/Galka.png")]
        else:
            self.fire = [pygame.image.load("Cheshuya/Sprites/krest.png")]
        for scale in (5, 10, 20):
            self.fire.append(pygame.transform.scale(self.fire[0], (scale, scale)))
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()
        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos
        self.gravity = 1

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(screen_rect):
            self.kill()


def create_particles(position, condition):
    particle_count = 20
    numbers = range(-5, 6)
    for i in range(particle_count):
        Particle(position, condition, random.choice(numbers), random.choice(numbers))


if __name__ == '__main__':
    pygame.init()
    size = width, height = 960, 480
    screen = pygame.display.set_mode(size)
    all_sprites = pygame.sprite.Group()
    stone_sprites = pygame.sprite.Group()
    brokenStones = pygame.sprite.Group()
    enter_sprites = pygame.sprite.Group()
    level_sprites = pygame.sprite.Group()
    pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))
    pygame.mixer.music.load('Cheshuya/music.wav')
    # pygame.mixer.music.play(-1)
    # pygame.mixer.music.set_volume(0.1)
    hub = Hub()