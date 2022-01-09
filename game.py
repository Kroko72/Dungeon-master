import pygame
import os
import math
import sys


# Функция закрытия
def terminate():
    pygame.quit()
    sys.exit()


# Функция загрузки изображения
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


# Начальное окно
def start_screen():
    intro_text = []

    fon = pygame.transform.scale(load_image('fon.png'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Проверка нажатия на кнопку START
                if 644 < event.pos[0] < 933 and 296 < event.pos[1] < 371:
                    return  # начинаем игру
                # Проверка нажатия на кнопку EXIT
                elif 640 < event.pos[0] < 933 and 394 < event.pos[1] < 469:
                    terminate()
        pygame.display.flip()
        clock.tick(FPS)


# Класс стрелы
class Arrow(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, mouse_x, mouse_y):
        super().__init__()
        self.image = load_image("arrow.png")
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
        self.x = mouse_x
        self.y = mouse_y
        self.speed = 5  # Начальная скорость
        self.angle = math.atan2(pos_y-mouse_y, pos_x-mouse_x)   # Угол наклона
        self.vel_x = math.cos(self.angle) * self.speed  # Скорость по иксу
        self.vel_y = math.sin(self.angle) * self.speed  # Скорость по игрику
        self.angle_degree = math.degrees(self.angle)  # Угол наклона в градусах
        #if self.angle_degree < 90:
        print(self.angle_degree)
        #self.image = pygame.transform.rotate(self.image, math.degrees(self.angle))

    def update(self):
        self.rect.x -= int(self.vel_x)
        self.rect.y -= int(self.vel_y)


# Инициализация пайгейма
pygame.init()

# Загрузка музыки и её воспроизведение
pygame.mixer.music.load("data/menu.ogg")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)

# Создание главного окна
size = width, height = 1530, 790
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Dungeon Master')
running = True

# Создание часов(ограничителя количества кадров)
FPS = 60
clock = pygame.time.Clock()

# Спрайт героя
all_sprites = pygame.sprite.Group()
sprite = pygame.sprite.Sprite()
sprite.image = load_image("try.png", -1)
sprite.rect = sprite.image.get_rect()
sprite.rect.x = 770
sprite.rect.y = 660
hero_speed = 2
all_sprites.add(sprite)

# Спрайт стрелы
arrow_group = pygame.sprite.Group()

# Запуск начального окна
start_screen()

# Задний фон игры
bg = load_image("1.png")

# Главный игровой цикл
while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = pygame.mouse.get_pos()
                arrow_group.add(Arrow(sprite.rect.x, sprite.rect.y, x, y))

    # Перемещение персонажа
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        if sprite.rect.x > 30:
            sprite.rect.x -= hero_speed
    if keys[pygame.K_d]:
        if sprite.rect.x < 1465:
            sprite.rect.x += hero_speed
    if keys[pygame.K_w]:
        if sprite.rect.y > 30:
            sprite.rect.y -= hero_speed
    if keys[pygame.K_s]:
        if sprite.rect.y < 720:
            sprite.rect.y += hero_speed

    screen.blit(bg, (0, 0))
    all_sprites.draw(screen)
    arrow_group.draw(screen)
    arrow_group.update()
    pygame.display.flip()
    clock.tick(FPS)