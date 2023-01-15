import pygame
import sqlite3
import random
import sys
ZOOMconst = 3  # константа для приближения экрана в мини-игре
screen_rect = (0, 0, 900, 800)  # константа размера экрана для партиклов


class Hub():  # экран для выбора сложности новой мини-игры
    def __init__(self):
        self.startScreen()  # вызываем начальный экран
        fade = pygame.Surface((960, 480))
        fade.fill((0, 0, 0))
        clock = pygame.time.Clock()
        background = pygame.image.load("Cheshuya/Sprites/Hub.jpg")
        back = pygame.sprite.Sprite()
        back.image = background
        back.rect = back.image.get_rect()
        back.rect.x = 0
        back.rect.y = 0
        all_sprites.add(back)  # фон
        dinoImage = pygame.image.load("Cheshuya/Sprites/DinoSprites - mort.png")
        coords = [(40, 200), (200, 300), (800, 200)]  # координаты камней
        dino = Dino(dinoImage, 24, 1, 480, 300, self)  # динозаврик
        self.end = EndGame(650, 250, dino)
        all_sprites.add(self.end)  # статуя конца игры
        all_sprites.add(dino)
        all_sprites.update()
        con = sqlite3.connect("Cheshuya/PlayersData.db")
        cur = con.cursor()
        level = cur.execute(f"""SELECT current FROM Player""").fetchall()[0][0]  # текущий уровень
        con.close()
        if level < 4:  # еще не конец игры
            for i in range(3):  # добавляем камни
                stone = Stone(coords[i][0], coords[i][1], i + 1, dino)
                stone_sprites.add(stone)
        else:
            for i in range(3):  # добавляем сломанные камни
                stone = BrokenStone(coords[i][0], coords[i][1] + 40)
                brokenStones.add(stone)
        stone_sprites.update()
        all_sprites.draw(screen)
        stone_sprites.draw(screen)
        screen2 = screen.copy()
        for a in range(300, 0, -1):  # выходим из затемнения
            screen1 = screen2.copy()
            fade.set_alpha(a)
            screen1.blit(fade, (0, 0))
            screen.blit(screen1, (0, 0))
            pygame.display.update()
            pygame.time.delay(5)
        running = True
        just_quit = False
        while running:  # основной цикл
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    just_quit = True
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
        if just_quit:
            sys.exit()  # выход без фин. экрана
        self.endScreen()

    def startScreen(self):  # начальный экран
        backgroundFirst = pygame.image.load("Cheshuya/Sprites/cave.jpg")
        back = pygame.sprite.Sprite()
        back.image = backgroundFirst
        back.rect = back.image.get_rect()
        back.rect.x = 0
        back.rect.y = 0
        all_sprites.add(back)  # фон
        press_space = pygame.image.load("Cheshuya/Sprites/press_space.png")
        space = pygame.sprite.Sprite()
        space.image = press_space
        space.rect = back.image.get_rect()
        space.rect.x = 280
        space.rect.y = 300  # "нажмите на пробел"
        start_game = pygame.image.load("Cheshuya/Sprites/start_game.png")
        start = pygame.sprite.Sprite()
        start.image = start_game
        start.rect = back.image.get_rect()
        start.rect.x = 250
        start.rect.y = 150  # название игры
        all_sprites.add(space)
        all_sprites.add(start)
        running = True
        while running:  # ждем нажатия на пробел
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
        for a in range(0, 300):  # красивое затемнение
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

    def endScreen(self):  # конец игры
        self.end.enter = False
        font = pygame.font.SysFont('Consolas', 32)
        con = sqlite3.connect("Cheshuya/PlayersData.db")
        cur = con.cursor()
        a = cur.execute('''SELECT score FROM Player''').fetchone()  # получаем счет
        des = font.render(f"Your score {a[0]}", 1, (0, 254, 255))  # счет для рисования на экране
        backgroundFirst = pygame.image.load("Cheshuya/Sprites/cave.jpg")
        back = pygame.sprite.Sprite()
        back.image = backgroundFirst
        back.rect = back.image.get_rect()
        back.rect.x = 0
        back.rect.y = 0
        all_sprites.add(back)  # фон
        thankyou = pygame.image.load("Cheshuya/Sprites/thanks.png")
        thank = pygame.sprite.Sprite()
        thank.image = thankyou
        thank.rect = back.image.get_rect()
        thank.rect.x = 250
        thank.rect.y = 100  # "спасибо за внимание"
        cr = pygame.image.load("Cheshuya/Sprites/Creators.png")
        creators = pygame.sprite.Sprite()
        creators.image = cr
        creators.rect = back.image.get_rect()
        creators.rect.x = 250
        creators.rect.y = 500  # создатели
        x = 250
        y = 700
        all_sprites.add(creators)
        all_sprites.add(thank)
        running = True
        clock = pygame.time.Clock()
        while running:  # прокрутка титров
            if creators.rect.y != 100:
                creators.rect = creators.rect.move(0, -1)
            x += 10
            y += 10
            screen.blit(des, (100, 100))
            thank.rect = thank.rect.move(0, -1)
            clock.tick(50)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    running = False
            all_sprites.draw(screen)
            all_sprites.update()
            pygame.display.flip()
            pygame.display.update()
        screen2 = screen.copy()
        fade = pygame.Surface((960, 480))
        fade.fill((0, 0, 0))
        for a in range(0, 300):  # затемнение
            screen1 = screen2.copy()
            fade.set_alpha(a)
            screen1.blit(fade, (0, 0))
            screen.blit(screen1, (0, 0))
            pygame.display.update()
        pygame.time.delay(5)
        screen.fill((0, 0, 0))
        all_sprites.remove(back)
        run = True
        while run:  # показываем счет до нажатия на пробел
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        run = False
            screen.blit(des, (370, 200))
            pygame.display.update()
        cur.execute("""UPDATE Player
                        SET current = 1""")
        cur.execute("""UPDATE Player
                        SET score = 0""")
        con.commit()  # подготовка БД для следующей игры
        sys.exit()  # выход из игры

    def nowhereToEnter(self):  # удаление всех камней и возможность завершить игру
        self.end.enter = True  #
        for sprite in stone_sprites:
            stone_sprites.remove(sprite)
            brokenStone = BrokenStone(sprite.x, sprite.y + 40)
            brokenStones.add(brokenStone)


class Dino(pygame.sprite.Sprite):  # миленький динозаврик
    def __init__(self, sheet, columns, rows, x, y, hub):
        super().__init__(all_sprites)
        self.clock = pygame.time.Clock()
        self.framesRun = []  # бег
        self.framesRunLeft = []  # бег влево
        self.framesIdle = []  # спокойствие
        self.framesIdleLeft = []  # спокойствие влево
        self.cut_sheet(sheet, columns, rows)  # нарезаем спрайты для анимации
        self.cur_frame = 0
        self.image = self.framesIdle[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.face = 'right'
        self.last = 'idle'
        self.hub = hub

    def cut_sheet(self, sheet, columns, rows):  # нарезка спрайтов
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
            self.framesIdleLeft.append(pygame.transform.flip(image, True, False))  # спокойствие влево
        for image in self.framesRun:
            self.framesRunLeft.append(pygame.transform.flip(image, True, False))  # бег влево

    def update(self):
        keys = pygame.key.get_pressed()  # нажатые клавиши
        idle = True
        if keys[pygame.K_RETURN]:
            a = self.checkCollide()  # проверка коллизий
            if a == 'end_game':
                self.hub.endScreen()  # конец игры
            if a:
                level = Level(a)  # уровень
                level_sprites.empty()
                screen = pygame.display.set_mode((960, 480))
                if level.end:  # делаем доступным конец игры
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
        # движение динозаврика выше
        # ниже находится выбор спрайта при беге/спокойствии
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
        self.image = pygame.transform.scale(self.image, (100, 100))  # изменение размера изображения

    def move(self, x, y):  # движение
        self.rect = self.rect.move(x, y)

    def checkCollide(self):  # проверка коллизий
        a = pygame.sprite.collide_mask(self, self.hub.end)
        if a and self.hub.end.enter:  # коллизия динозаврика с *активированной* статуей
            return 'end_game'
        for sprite in stone_sprites:
            a = pygame.sprite.collide_mask(self, sprite)  # коллизия динозаврика с камнем
            if a:
                return sprite.hard  # возвращаем сложность
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
                        3:  ('Cheshuya/Sprites/hard.png', 0)}  # картинки сложностей

    def update(self):
        enter_sprites.empty()
        a = pygame.sprite.collide_mask(self, self.dino)  # коллизия с динозавриком
        if a:
            setting = pygame.sprite.Sprite()
            setting.image = pygame.image.load(self.settings[self.hard][0])
            setting.rect = setting.image.get_rect()
            setting.rect.x = self.x + self.settings[self.hard][1]
            setting.rect.y = self.y - 50
            enter_sprites.add(setting)
            enter_sprites.update()
            enter_sprites.draw(screen)  # рисуем надпись со сложностью


class BrokenStone(pygame.sprite.Sprite):  # сломанный камень
    def __init__(self, x, y):
        super().__init__(brokenStones)
        self.image = pygame.image.load("Cheshuya/Sprites/BrokenStone.png")
        self.x, self.y = x, y
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)  # обычное создание спрайта без каких-либо особенностей


class EndGame(pygame.sprite.Sprite):  # статуя конца игры
    def __init__(self, x, y, dino):
        super().__init__(all_sprites)
        self.image = pygame.image.load("Cheshuya/Sprites/Shop.png")
        self.x, self.y = x, y
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)
        self.dino = dino
        self.enter = False  # активация

    def update(self):
        if self.enter:  # если активирована
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
                enter_sprites.draw(screen)  # рисуем надпись enter


class Level():  # уровень
    def __init__(self, hard):
        self.end = False
        current = 0  # номер элемента, который нужно найти
        screen = pygame.display.set_mode((900, 800))
        con = sqlite3.connect("Cheshuya/PlayersData.db")
        cur = con.cursor()
        result = cur.execute(f"""SELECT * FROM Player""").fetchall()
        con.close()
        level, score = result[0][1], result[0][0]  # текущий уровень и счет
        background = pygame.image.load(f"Cheshuya/Levels/level{level}.jpg")
        back = pygame.sprite.Sprite()
        back.image = background
        back.rect = back.image.get_rect()
        back.rect.x = 0
        back.rect.y = 0  # основная картинка
        need_images = []
        for i in range(1, 6):
            need_images.append(f"Cheshuya/Levels/level{level}.{i}.png")  # нужные элементы
        f = open(f'Cheshuya/Levels/hitboxes{level}.txt', mode='rt', encoding='utf-8')
        hitboxes = eval(f.readlines()[0])  # координаты элементов
        f.close()
        need = pygame.sprite.Sprite()
        need.image = pygame.image.load(need_images[0])
        need.rect = need.image.get_rect()
        need.rect.x = 0
        need.rect.y = 550  # спрайт нужного элемента
        screen2  = pygame.Surface((900, 800))
        hit = pygame.sprite.Group()
        hitbox = pygame.sprite.Sprite()
        hitbox.image = pygame.image.load(need_images[0])
        hitbox.rect = hitboxes[0]  # хитбоксы
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
        if hard == 1:  # количество сердец и секунд, в зависимости от уровня сложности
            counter = 120
            hearts_count = 3
        elif hard == 2:
            counter = 90
            hearts_count = 2
        elif hard == 3:
            counter = 60
            hearts_count = 1
        for i in range(hearts_count):  # добавляем сердца
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
        while running:  # основной цикл
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.USEREVENT:  # уменьшение секунд на таймере
                    counter -= 1
                    if counter > 0:
                        text = str(counter)
                    else:
                        res = 'lose'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 3:
                        if zoom1:  # отменить зум
                            zoom1 = False
                        else:  # подтвердить зум
                            zoom1 = True
                    elif event.button == 1:  # ответ
                        x, y = arrow.rect.x, arrow.rect.y
                        a = pygame.sprite.collide_mask(arrow, hitbox)
                        if a:  # верное нажатие
                            good.play()
                            create_particles((x, y), True)
                            current += 1
                            if current == len(need_images):
                                res = 'win'
                            else:
                                need.image = pygame.image.load(need_images[current])
                                hitbox.image = pygame.image.load(need_images[current])
                                hitbox.rect = hitboxes[current]
                        else:  # неверное
                            bad.play()
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
                arrow.rect.y = y  # спрайт стрелки
            screen.fill((0, 0, 0))
            hearts_sprites.draw(screen)
            hearts_sprites.update()
            level_sprites.draw(screen)
            level_sprites.update()
            screen.blit(font.render(text, True, (255, 255, 255)), (700, 600))
            hit.draw(screen2)
            screen2.set_alpha(0)
            screen.blit(screen2, (0, 0))
            if zoom1 and xMouse != 0 and yMouse != 0:  # возможность двигать камеру в зуме (WASD)
                keys = pygame.key.get_pressed()
                if keys[pygame.K_a]:
                    xMouse -= 5
                elif keys[pygame.K_d]:
                    xMouse += 5
                elif keys[pygame.K_w]:
                    yMouse -= 5
                elif keys[pygame.K_s]:
                    yMouse += 5
            if zoom1:  # зум
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
        if res == 'win':  # победа
            plusScore = hard * 10
            con = sqlite3.connect("Cheshuya/PlayersData.db")
            cur = con.cursor()
            cur.execute(f"""UPDATE Player
                            SET current = current + 1""")
            cur.execute(f"""UPDATE Player
                            SET score = score + {plusScore}""")
            con.commit()
            con.close()
            if level == 3:
                self.end = True


class Particle(pygame.sprite.Sprite):  # партиклы
    def __init__(self, pos, condition, dx=random.choice(range(-6, 5)), dy=random.choice(range(-6, 5))):
        super().__init__(level_sprites)
        if condition:
            self.fire = [pygame.image.load("Cheshuya/Sprites/Galka.png")]  # галочки
        else:
            self.fire = [pygame.image.load("Cheshuya/Sprites/krest.png")]  # крестики
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


def create_particles(position, condition):  # создание партиклов
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
    pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))   # прячем курсор
    pygame.mixer.music.load('Cheshuya/music.wav')
    pygame.mixer.music.play(-1)  # музыка
    pygame.mixer.music.set_volume(0.1)
    good = pygame.mixer.Sound('Cheshuya/good.mp3')  # звук правильного нажатия
    bad = pygame.mixer.Sound('Cheshuya/bad.mp3')  # звук неправильного нажатия
    hub = Hub()  # начало игры (хаб)
