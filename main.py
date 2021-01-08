import pygame
import sys
import os

all_sprites = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()


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
    intro_text = ["Игра ПИНГ ПОНГ", "",
                  "Для начала нажмите любую кнопку",
                  "Для руководства нажмите R",
                  "Пробная версия 0.00000000001"]

    fon = pygame.transform.scale(load_image('fon.png'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 220
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('blue'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
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
        clock.tick(30)


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
    clock = pygame.time.Clock()
    running = True
    flag = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if flag == 0:
            flag = start_screen()
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        horizontal_borders.draw(screen)
        vertical_borders.draw(screen)
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()
    main()
