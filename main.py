import pygame


class Hub():
    def __init__(self, screen):
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
        stoneImage = pygame.image.load("Cheshuya/Sprites/stone.png")
        coords = [(40, 200), (200, 300), (800, 200)]
        for i in range(3):
            stone = pygame.sprite.Sprite()
            stone.image = stoneImage
            stone.rect = stone.image.get_rect()
            stone.rect.x = coords[i][0]
            stone.rect.y = coords[i][1]
            all_sprites.add(stone)
        dino = Dino(dinoImage, 24, 1, 480, 300)
        all_sprites.add(dino)
        all_sprites.update()
        all_sprites.draw(screen)
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
        self.frames = []
        self.framesLeft = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.face = 'right'

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))
        for image in self.frames:
            self.framesLeft.append(pygame.transform.flip(image, True, False))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        keys = pygame.key.get_pressed()
        idle = True
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
        self.clock.tick(60)
        if self.face == 'left':
            self.image = self.framesLeft[self.cur_frame]
        else:
            self.image = self.frames[self.cur_frame]
        self.image = pygame.transform.scale(self.image, (100, 100))

    def move(self, x, y):
        self.rect = self.rect.move(x, y)


if __name__ == '__main__':
    pygame.init()
    size = width, height = 960, 480
    screen = pygame.display.set_mode(size)
    all_sprites = pygame.sprite.Group()
    pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))
    hub = Hub(screen)
