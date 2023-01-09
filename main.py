import pygame
import sqlite3


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
        shopImage = pygame.image.load("Cheshuya/Sprites/Shop.png")
        shop = pygame.sprite.Sprite()
        shop.image = shopImage
        shop.rect = shop.image.get_rect()
        shop.rect.x = 650
        shop.rect.y = 250
        all_sprites.add(shop)
        dinoImage = pygame.image.load("Cheshuya/Sprites/DinoSprites - mort.png")
        stoneImage = pygame.image.load("Cheshuya/Sprites/stone.png")
        coords = [(40, 200), (200, 300), (800, 200)]
        dino = Dino(dinoImage, 24, 1, 480, 300)
        all_sprites.add(dino)
        all_sprites.update()
        for i in range(3):
            stone = Stone(coords[i][0], coords[i][1], i + 1, dino)
            stone_sprites.add(stone)
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


class Dino(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
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
            print(self.checkCollide())
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
        if (self.last == 'idle' and idle) or (self.last == 'run' and not(idle)):  # TODO: изменить логику, слишком кринжово
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
        for sprite in stone_sprites:
            a = pygame.sprite.collide_mask(self, sprite)
            if a:
                stone_sprites.remove(sprite)
                brokenStone = BrokenStone(sprite.x, sprite.y + 40)
                brokenStones.add(brokenStone)
                return sprite.level
        return False


class Stone(pygame.sprite.Sprite):  # камень с рунами
    def __init__(self, x, y, level, dino):
        super().__init__(stone_sprites)
        self.image = pygame.image.load("Cheshuya/Sprites/stone.png")
        self.x, self.y = x, y
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)
        self.level = level
        self.dino = dino

    def update(self):
        enter_sprites.empty()
        a = pygame.sprite.collide_mask(self, self.dino)
        if a:
            enter = pygame.sprite.Sprite()
            enter.image = pygame.image.load("Cheshuya/Sprites/enter.png")
            enter.rect = enter.image.get_rect()
            enter.rect.x = self.x - 15
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


class Level():  # уровень
    pass


if __name__ == '__main__':
    pygame.init()
    size = width, height = 960, 480
    screen = pygame.display.set_mode(size)
    all_sprites = pygame.sprite.Group()
    stone_sprites = pygame.sprite.Group()
    brokenStones = pygame.sprite.Group()
    enter_sprites = pygame.sprite.Group()
    pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))
    hub = Hub()