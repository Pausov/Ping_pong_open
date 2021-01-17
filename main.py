import pygame
import sys
import os
import random
import pygame.locals
import time

all_sprites = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()


class Ball(pygame.sprite.Sprite):
    def __init__(self, radius, x, y):
        super().__init__(all_sprites)
        self.radius = radius
        self.image = pygame.Surface((2 * radius, 2 * radius),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("red"),
                           (radius, radius), radius)
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        self.vx = random.choice([-2, -1, 1, 2])
        self.vy = random.choice([-2, -1, 1, 2])
        self.f1 = pygame.font.Font('counter.ttf', 50)
        self.count_l = 0
        self.count_r = 0
        self.c_l = self.f1.render('{}'.format(self.count_l), True,
                                  (255, 255, 255))
        self.c_r = self.f1.render('{}'.format(self.count_r), True,
                                  (255, 255, 255))

    def counter(self, x):
        if x == 'l':
            self.count_r += 1
        elif x == 'r':
            self.count_l += 1
        count_sound.play()
        time.sleep(0.5)
        self.rect.x = width // 2
        self.rect.y = height // 2
        self.vx = random.choice([-2, -1, 1, 2])
        self.vy = random.choice([-2, -1, 1, 2])

    def update(self):
        self.c_l = self.f1.render('{}'.format(self.count_l), True,
                                  (255, 255, 255))
        self.c_r = self.f1.render('{}'.format(self.count_r), True,
                                  (255, 255, 255))
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
            hit_sound.play()

        if pygame.sprite.spritecollideany(self, vertical_borders):
            if 1 < self.rect.x < width - 19:
                hit_sound.play()
            self.vx = -self.vx + random.choice([-2, -1, 1, 2])
        if self.rect.x <= 1:
            Ball.counter(self, 'l')
        if self.rect.x >= width - 19:
            Ball.counter(self, 'r')
        screen.blit(self.c_l, (width * 0.4, 40))
        screen.blit(self.c_r, (width * 0.56, 40))


class Platfomes(pygame.sprite.Sprite):
    def __init__(self, w, h, x, y):
        self.y = y
        self.x = x
        super().__init__(all_sprites)
        if x < width // 2:
            self.add(vertical_borders)
        else:
            self.add(vertical_borders)
        self.image = pygame.Surface([w, h])
        self.rect = pygame.Rect(self.x, self.y, w, h)
        self.image.fill((255, 255, 255))

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] and self.x > width // 2:
            self.rect = self.rect.move(0, -4)
        if keys[pygame.K_DOWN] and self.x > width // 2:
            self.rect = self.rect.move(0, 4)

        if keys[pygame.K_w] and self.x < width // 2:
            self.rect = self.rect.move(0, -4)
        if keys[pygame.K_s] and self.x < width // 2:
            self.rect = self.rect.move(0, 4)

        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= height:
            self.rect.bottom = height


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)
        self.image.fill((255, 255, 255))


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print('Not found')
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey)
        else:
            image = image.convert_alpha()
    return image


def start_screen():
    intro_text = ["Для начала нажмите",
                  'Нажмите любую кнопку',
                  "Для руководства",
                  "нажмите R",
                  "Пробная версия 0.00000000001"]

    fon = pygame.transform.scale(load_image('fon.png'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 202
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 4
        intro_rect.top = text_coord
        intro_rect.x = 274
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return 1
        pygame.display.flip()
        clock.tick(40)


def main():
    pass


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Ping_pong')
    size = width, height = 800, 500
    screen = pygame.display.set_mode(size)
    Border(0, 0, width - 1, 0)
    Border(0, height - 1, width, height)
    Border(0, 0, 0, height)
    Border(width - 1, 0, width - 1, height - 1)
    Platfomes(10, 50, 750, 250)
    Platfomes(10, 50, 50, 250)
    hit_sound = pygame.mixer.Sound('Pong.wav')
    count_sound = pygame.mixer.Sound('count.wav')
    clock = pygame.time.Clock()
    running = True
    flag = 0
    count = 0
    pygame.draw.line(screen, 'white', (width // 2, 0), (width // 2, height))
    while running:
        if flag == 1 and count == 0:
            Ball(9, width // 2, height // 2)
            count = 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if flag == 0:
            flag = start_screen()
        screen.fill((0, 0, 0))
        pygame.draw.line(screen, 'white', (width // 2, 0), (width // 2, height), 3)
        all_sprites.draw(screen)
        horizontal_borders.draw(screen)
        vertical_borders.draw(screen)
        all_sprites.update()
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
    main()
