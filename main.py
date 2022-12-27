import pygame


class Hub():
    def __init__(self, screen):
        im = pygame.image.load("DinoSprites - mort.png")
        dino = Dino(im, 24, 1, 50, 50)
        all_sprites.add(dino)
        running = True
        clock = pygame.time.Clock()
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
        if keys[pygame.K_a]:
            self.move(-20, 0)
            self.face = 'left'
        elif keys[pygame.K_d]:
            self.move(20, 0)
            self.face = 'right'
        if keys[pygame.K_w]:
            self.move(0, -20)
        elif keys[pygame.K_s]:
            self.move(0, 20)
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
    size = width, height = 400, 400
    screen = pygame.display.set_mode(size)
    all_sprites = pygame.sprite.Group()
    hub = Hub(screen)
