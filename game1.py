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
        self.angle = math.atan2(pos_y - mouse_y, pos_x - mouse_x)  # Угол наклона
        self.vel_x = math.cos(self.angle) * self.speed  # Скорость по иксу
        self.vel_y = math.sin(self.angle) * self.speed  # Скорость по игрику
        self.angle_degree = math.degrees(self.angle)  # Угол наклона в градусах
        # if self.angle_degree < 90:
        print(self.angle_degree)
        # self.image = pygame.transform.rotate(self.image, math.degrees(self.angle))

    def update(self):
        self.rect.x -= int(self.vel_x)
        self.rect.y -= int(self.vel_y)


# Инициализация пайгейма
pygame.init()

# Загрузка музыки и её воспроизведение
pygame.mixer.music.load("data/menu.ogg")
pygame.mixer.music.set_volume(0.1)
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
sprite.image = load_image("arrow.png", -1)
sprite.image = pygame.transform.scale(sprite.image, (1, 1))

# Спрайт героя идущего налево
sprite.imageL1 = load_image('3.png', -1)
sprite.imageL1 = pygame.transform.scale(sprite.imageL1, (45, 65))

sprite.imageL2 = load_image('31.png', -1)
sprite.imageL2 = pygame.transform.scale(sprite.imageL2, (45, 65))

sprite.imageL3 = load_image('32.png', -1)
sprite.imageL3 = pygame.transform.scale(sprite.imageL3, (45, 57))

sprite.imageL4 = load_image('33.png', -1)
sprite.imageL4 = pygame.transform.scale(sprite.imageL4, (45, 68))

sprite.imageL5 = load_image('34.png', -1)
sprite.imageL5 = pygame.transform.scale(sprite.imageL5, (45, 65))

# Спрайт героя идущего вправо
sprite.imageR1 = load_image('4.png', -1)
sprite.imageR1 = pygame.transform.scale(sprite.imageR1, (50, 60))

sprite.imageR2 = load_image('41.png', -1)
sprite.imageR2 = pygame.transform.scale(sprite.imageR2, (45, 57))

sprite.imageR3 = load_image('42.png', -1)
sprite.imageR3 = pygame.transform.scale(sprite.imageR3, (50, 57))

sprite.imageR4 = load_image('43.png', -1)
sprite.imageR4 = pygame.transform.scale(sprite.imageR4, (45, 57))

sprite.imageR5 = load_image('44.png', -1)
sprite.imageR5 = pygame.transform.scale(sprite.imageR5, (50, 68))

# Спрайт героя идущего вперед
sprite.imageF1 = load_image('hero.png', -1)
sprite.imageF1 = pygame.transform.scale(sprite.imageF1, (45, 57))

sprite.imageF2 = load_image('hero1.png', -1)
sprite.imageF2 = pygame.transform.scale(sprite.imageF2, (45, 57))

sprite.imageF3 = load_image('hero2.png', -1)
sprite.imageF3 = pygame.transform.scale(sprite.imageF3, (45, 63))

sprite.imageF4 = load_image('hero3.png', -1)
sprite.imageF4 = pygame.transform.scale(sprite.imageF4, (45, 62))

sprite.imageF5 = load_image('hero4.png', -1)
sprite.imageF5 = pygame.transform.scale(sprite.imageF5, (45, 68))

# Спрайт героя идущего назад
sprite.imageB1 = load_image('2.png', -1)
sprite.imageB1 = pygame.transform.scale(sprite.imageB1, (45, 61))

sprite.imageB2 = load_image('21.png', -1)
sprite.imageB2 = pygame.transform.scale(sprite.imageB2, (45, 66))

sprite.imageB3 = load_image('22.png', -1)
sprite.imageB3 = pygame.transform.scale(sprite.imageB3, (45, 63))

sprite.imageB4 = load_image('23.png', -1)
sprite.imageB4 = pygame.transform.scale(sprite.imageB4, (45, 59))

sprite.imageB5 = load_image('24.png', -1)
sprite.imageB5 = pygame.transform.scale(sprite.imageB5, (45, 63))

# спрайт стоящего на месте игрока
sprite.stopPlayer = load_image('01.png', -1)
sprite.stopPlayer = pygame.transform.scale(sprite.stopPlayer, (45, 61))

# спрайт идущего вверх налево
sprite.imageFL1 = load_image('6.png', -1)
sprite.imageFL1 = pygame.transform.scale(sprite.imageFL1, (45, 61))

sprite.imageFL2 = load_image('61.png', -1)
sprite.imageFL2 = pygame.transform.scale(sprite.imageFL2, (45, 61))

sprite.imageFL3 = load_image('62.png', -1)
sprite.imageFL3 = pygame.transform.scale(sprite.imageFL3, (45, 61))

sprite.imageFL4 = load_image('63.png', -1)
sprite.imageFL4 = pygame.transform.scale(sprite.imageFL4, (45, 61))

sprite.imageFL5 = load_image('64.png', -1)
sprite.imageFL5 = pygame.transform.scale(sprite.imageFL5, (45, 61))

# спрайт идущего вверх направо
sprite.imageFR1 = load_image('5.png', -1)
sprite.imageFR1 = pygame.transform.scale(sprite.imageFR1, (45, 61))

sprite.imageFR2 = load_image('51.png', -1)
sprite.imageFR2 = pygame.transform.scale(sprite.imageFR2, (45, 61))

sprite.imageFR3 = load_image('52.png', -1)
sprite.imageFR3 = pygame.transform.scale(sprite.imageFR3, (45, 61))

sprite.imageFR4 = load_image('53.png', -1)
sprite.imageFR4 = pygame.transform.scale(sprite.imageFR4, (45, 61))

sprite.imageFR5 = load_image('54.png', -1)
sprite.imageFR5 = pygame.transform.scale(sprite.imageFR5, (45, 61))

# спрайт идущего вниз налево
sprite.imageBL1 = load_image('7.png', -1)
sprite.imageBL1 = pygame.transform.scale(sprite.imageBL1, (45, 61))

sprite.imageBL2 = load_image('71.png', -1)
sprite.imageBL2 = pygame.transform.scale(sprite.imageBL2, (45, 61))

sprite.imageBL3 = load_image('72.png', -1)
sprite.imageBL3 = pygame.transform.scale(sprite.imageBL3, (45, 61))

sprite.imageBL4 = load_image('73.png', -1)
sprite.imageBL4 = pygame.transform.scale(sprite.imageBL4, (45, 61))

sprite.imageBL5 = load_image('74.png', -1)
sprite.imageBL5 = pygame.transform.scale(sprite.imageBL5, (45, 61))

# спрайт идущего вниз направо
sprite.imageBR1 = load_image('01.png', -1)
sprite.imageBR1 = pygame.transform.scale(sprite.imageBR1, (45, 61))

sprite.imageBR2 = load_image('12.png', -1)
sprite.imageBR2 = pygame.transform.scale(sprite.imageBR2, (45, 61))

sprite.imageBR3 = load_image('13.png', -1)
sprite.imageBR3 = pygame.transform.scale(sprite.imageBR3, (45, 61))

sprite.imageBR4 = load_image('14.png', -1)
sprite.imageBR4 = pygame.transform.scale(sprite.imageBR4, (45, 61))

sprite.imageBR5 = load_image('15.png', -1)
sprite.imageBR5 = pygame.transform.scale(sprite.imageBR5, (45, 61))

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

# Переменные необходимые для анимации

right = False
left = False
forward = False
back = False
fr = False
fl = False
br = False
bl = False
animCount = 0

Right = [sprite.imageR1, sprite.imageR2, sprite.imageR3, sprite.imageR1, sprite.imageR4, sprite.imageR5]

Left = [sprite.imageL1, sprite.imageL2, sprite.imageL3, sprite.imageL1, sprite.imageL4, sprite.imageL5]

Forward = [sprite.imageF1, sprite.imageF2, sprite.imageF3, sprite.imageF1, sprite.imageF4, sprite.imageF5]

Back = [sprite.imageB1, sprite.imageB2, sprite.imageB3, sprite.imageB1, sprite.imageB4, sprite.imageB5]

FL = [sprite.imageFL1, sprite.imageFL2, sprite.imageFL3, sprite.imageFL1, sprite.imageFL4, sprite.imageFL5]

FR = [sprite.imageFR1, sprite.imageFR2, sprite.imageFR3, sprite.imageFR1, sprite.imageFR4, sprite.imageFR5]

BL = [sprite.imageBL1, sprite.imageBL2, sprite.imageBL3, sprite.imageBL1, sprite.imageBL4, sprite.imageBL5]

BR = [sprite.imageBR1, sprite.imageBR2, sprite.imageBR3, sprite.imageBR1, sprite.imageBR4, sprite.imageBR5]


# Функция отрисовки персонажа

def drawPlayer():
    global animCount
    screen.blit(bg, (0, 0))
    if animCount + 1 >= 60:
        animCount = 0
    if left:
        screen.blit(Left[animCount // 12], (sprite.rect.x, sprite.rect.y))
        animCount += 1
    elif right:
        screen.blit(Right[animCount // 12], (sprite.rect.x, sprite.rect.y))
        animCount += 1
    elif forward:
        screen.blit(Forward[animCount // 12], (sprite.rect.x, sprite.rect.y))
        animCount += 1
    elif back:
        screen.blit(Back[animCount // 12], (sprite.rect.x, sprite.rect.y))
        animCount += 1
    elif fr:
        screen.blit(FR[animCount // 12], (sprite.rect.x, sprite.rect.y))
        animCount += 1
    elif fl:
        screen.blit(FL[animCount // 12], (sprite.rect.x, sprite.rect.y))
        animCount += 1
    elif bl:
        screen.blit(BL[animCount // 12], (sprite.rect.x, sprite.rect.y))
        animCount += 1
    elif br:
        screen.blit(BR[animCount // 12], (sprite.rect.x, sprite.rect.y))
        animCount += 1
    else:
        screen.blit(sprite.stopPlayer, (sprite.rect.x, sprite.rect.y))

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
    if keys[pygame.K_w] and keys[pygame.K_a]:
        if sprite.rect.y > 30 and sprite.rect.x > 30:
            sprite.rect.y -= hero_speed
            sprite.rect.x -= hero_speed
            left = False
            right = False
            forward = False
            back = False
            fr = False
            fl = True
            br = False
            bl = False
    elif keys[pygame.K_w] and keys[pygame.K_d]:
        if sprite.rect.y > 30 and sprite.rect.x < 1465:
            sprite.rect.y -= hero_speed
            sprite.rect.x += hero_speed
            left = False
            right = False
            forward = False
            back = False
            fr = True
            fl = False
            br = False
            bl = False
    elif keys[pygame.K_s] and keys[pygame.K_a]:
        if sprite.rect.y < 720 and sprite.rect.x > 30:
            sprite.rect.y += hero_speed
            sprite.rect.x -= hero_speed
            left = False
            right = False
            forward = False
            back = False
            fr = False
            fl = False
            br = False
            bl = True
    elif keys[pygame.K_s] and keys[pygame.K_d]:
        if sprite.rect.y < 720 and sprite.rect.x < 1465:
            sprite.rect.y += hero_speed
            sprite.rect.x += hero_speed
            left = False
            right = False
            forward = False
            back = False
            fr = False
            fl = False
            br = True
            bl = False
    elif keys[pygame.K_a]:
        if sprite.rect.x > 30:
            left = True
            right = False
            forward = False
            back = False
            fr = False
            fl = False
            br = False
            bl = False
            sprite.rect.x -= hero_speed
    elif keys[pygame.K_d]:
        if sprite.rect.x < 1465:
            left = False
            right = True
            forward = False
            back = False
            fr = False
            fl = False
            br = False
            bl = False
            sprite.rect.x += hero_speed
    elif keys[pygame.K_w]:
        if sprite.rect.y > 30:
            sprite.rect.y -= hero_speed
            left = False
            right = False
            forward = True
            back = False
            fr = False
            fl = False
            br = False
            bl = False
    elif keys[pygame.K_s]:
        if sprite.rect.y < 720:
            sprite.rect.y += hero_speed
            left = False
            right = False
            forward = False
            back = True
            fr = False
            fl = False
            br = False
            bl = False
    else:
        forward = False
        back = False
        left = False
        right = False
        fr = False
        fl = False
        br = False
        bl = False
        animCount = 0

    screen.blit(bg, (0, 0))
    all_sprites.draw(screen)
    drawPlayer()
    arrow_group.draw(screen)
    arrow_group.update()
    pygame.display.flip()
    clock.tick(FPS)
