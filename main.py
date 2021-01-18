import pygame
import sys
import os
import random
import pygame.locals
import time

all_sprites = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
star = pygame.sprite.Group()
platform_right = pygame.sprite.Group()
colors = [(255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255)]
colors_fon = []
current_color = 0
Rscore = 0
Lscore = 0
GRAVITY = 1


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
        global Rscore
        global Lscore
        if x == 'l':
            self.count_r += 1
            Rscore = self.count_r
        elif x == 'r':
            self.count_l += 1
            Lscore = self.count_l
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
            self.vx = -self.vx + random.choice([-1, 1, 2])
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
        global current_color
        super().__init__(all_sprites)
        self.add(vertical_borders)
        self.image = pygame.Surface([w, h])
        self.rect = pygame.Rect(self.x, self.y, w, h)
        self.image.fill(colors[current_color])

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
            self.add(platform_right)
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


class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    fire = [load_image("star.png")]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()
        self.add(star)

        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой (значение константы)
        self.gravity = GRAVITY

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if not self.rect.colliderect(screen_rect):
            self.kill()


def create_particles(position):
    # количество создаваемых частиц
    particle_count = 3
    # возможные скорости
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


def start_screen():
    keys = pygame.key.get_pressed()
    intro_text = ["Для начала нажмите",
                  'Нажмите любую кнопку']

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
        global current_color
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.type != pygame.K_r:
                return 1
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if current_color != len(colors) - 1:
                    current_color += 1
                else:
                    current_color = 1
        pygame.draw.rect(screen, colors[current_color], ((43, 249), (20, 100)))
        pygame.draw.rect(screen, colors[current_color], ((737, 240), (20, 100)))
        pygame.display.flip()
        clock.tick(40)


def ending():
    global Rscore
    global Lscore
    pygame.mixer_music.stop()
    win_sound.play()
    if Rscore == SCORE:
        win = 'Правого'
    else:
        win = 'Левого'
    intro_text = ['ПОБЕДА', win, 'Игрока']

    while True:
        global current_color
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.type != pygame.K_r:
                return 1
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if current_color != len(colors) - 1:
                    current_color += 1
                else:
                    current_color = 1
        fon = pygame.transform.scale(load_image('end.png'), (width, height))
        screen.blit(fon, (0, 0))
        create_particles((random.randint(1, 800), (random.randint(1, 500))))
        star.draw(screen)
        star.update()
        pygame.draw.rect(screen, colors[current_color], ((385, 130), (20, 100)))
        count = 0
        font = pygame.font.Font(None, 30)
        text_coord = 40
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coord += 4
            intro_rect.top = text_coord
            if count == 0:
                intro_rect.x = 350
            else:
                intro_rect.x = 360
            count = 1
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        pygame.display.flip()
        clock.tick(20)


def main():
    pass


if __name__ == '__main__':
    SCORE = 5
    pygame.init()
    pygame.mixer_music.load('music.wav')
    pygame.mixer_music.play(-1)
    pygame.display.set_caption('Ping_pong')
    size = width, height = 800, 500
    screen = pygame.display.set_mode(size)
    Border(0, 0, width - 1, 0)
    Border(0, height - 1, width, height)
    Border(0, 0, 0, height)
    Border(width - 1, 0, width - 1, height - 1)
    hit_sound = pygame.mixer.Sound('Pong.wav')
    win_sound = pygame.mixer.Sound('win.wav')
    count_sound = pygame.mixer.Sound('count.wav')
    clock = pygame.time.Clock()
    running = True
    screen_rect = (0, 0, width, height)
    flag = 0
    count = 0
    pygame.draw.line(screen, (255, 255, 255), (width // 2, 0), (width // 2, height))
    while running:
        if flag == 1 and count == 0:
            Ball(9, width // 2, height // 2)
            Platfomes(10, 50, 750, 250)
            Platfomes(10, 50, 50, 250)
            count = 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if flag == 0:
            flag = start_screen()
        if Rscore == SCORE or Lscore == SCORE:
            ending()
            create_particles((400, 400))
            star.update()

        screen.fill((0, 0, 0))
        pygame.draw.line(screen, (255, 255, 255), (width // 2, 0), (width // 2, height), 3)
        all_sprites.draw(screen)
        horizontal_borders.draw(screen)
        vertical_borders.draw(screen)
        platform_right.draw(screen)
        all_sprites.update()
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
    main()
