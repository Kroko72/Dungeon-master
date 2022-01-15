import math
import os
import sys
import pygame
import time


# Функция определения направления движения персонажа
def where_to_go(go_left=False, go_right=False, go_forward=False, go_back=False, f1=False, f2=False, b1=False, b2=False):
    global left, right, forward, back, forward_right, forward_left, back_right, back_left
    left = go_left
    right = go_right
    forward = go_forward
    back = go_back
    forward_right = f1
    forward_left = f2
    back_right = b1
    back_left = b2


# Функция отрисовки персонажа
def draw_player():
    global animCount, roll
    screen.blit(bg, (0, 0))
    if animCount + 1 >= 73:
        animCount = 0
        roll = False
    elif left:
        screen.blit(Left[animCount // 12], (sprite.rect.x, sprite.rect.y))
    elif right:
        if roll is True:
            screen.blit(roll_Right[animCount // 12], (sprite.rect.x, sprite.rect.y))
        else:
            screen.blit(Right[animCount // 12], (sprite.rect.x, sprite.rect.y))
    elif forward:
        screen.blit(Forward[animCount // 12], (sprite.rect.x, sprite.rect.y))
    elif back:
        screen.blit(Back[animCount // 12], (sprite.rect.x, sprite.rect.y))
    elif forward_right:
        screen.blit(FR[animCount // 12], (sprite.rect.x, sprite.rect.y))
    elif forward_left:
        screen.blit(FL[animCount // 12], (sprite.rect.x, sprite.rect.y))
    elif back_left:
        screen.blit(BL[animCount // 12], (sprite.rect.x, sprite.rect.y))
    elif back_right:
        screen.blit(BR[animCount // 12], (sprite.rect.x, sprite.rect.y))
    else:
        screen.blit(sprite.stopPlayer, (sprite.rect.x, sprite.rect.y))
    print(animCount // 12)
    animCount += 1


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
    intro_text = ["Ваш рекорд:", "", "лучшее время прохождения"]
    fon = pygame.transform.scale(load_image('fon.png'), (width, height))
    while True:
        screen.blit(fon, (0, 0))  # Заполнение фона начального экрана
        font = pygame.font.Font(None, 30)
        text_coord = 50
        # Текст рекорда на начальном экране
        for line in intro_text:
            string_rendered = font.render(line, True, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
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
        # Замена курсора
        if pygame.mouse.get_focused():
            screen.blit(cursor, pygame.mouse.get_pos())
        pygame.display.flip()
        clock.tick(FPS)


# Класс стрелы
class Arrow(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, mouse_x, mouse_y):
        super().__init__()
        global angle
        self.image = load_image("arrow.png", -1)
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
        self.speed = 10  # Начальная скорость
        self.angle = math.atan2(pos_y - mouse_y, pos_x - mouse_x)  # Угол наклона (направление стрелы)
        self.vel_x = math.cos(self.angle) * self.speed  # Скорость по иксу
        self.vel_y = math.sin(self.angle) * self.speed  # Скорость по игрику

        # Угол поворота картинки стрелы и её разворачивание в направлении её выпускания
        rel_x, rel_y = mouse_x - pos_x, mouse_y - pos_y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.image = pygame.transform.rotate(self.image, angle)

    def update(self):
        global old_arrow_x, old_arrow_y
        if 40 < self.rect.x < 1500 and 40 < self.rect.y < 760:
            if (self.rect.x - int(self.vel_x)) > 40 and (self.rect.y - int(self.vel_y)) > 40:
                self.rect.x -= int(self.vel_x)
                self.rect.y -= int(self.vel_y)
        old_arrow_x, old_arrow_y = self.rect.x, self.rect.y


# Класс стрелы, летящей назад
class ArrowBack(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, old_x, old_y):
        super().__init__()
        global angle
        self.image = load_image("arrow.png", -1)
        self.rect = self.image.get_rect(center=(old_x, old_y))
        self.speed = 10  # Начальная скорость
        self.angle = math.atan2(pos_y - self.rect.y, pos_x - self.rect.x)  # Угол наклона
        self.vel_x = math.cos(self.angle) * self.speed  # Скорость по иксу
        self.vel_y = math.sin(self.angle) * self.speed  # Скорость по игрику
        self.image = pygame.transform.rotate(self.image, angle + 180)  # Разворот стрелы в противоположную сторону

    def update(self):
        global where_y, where_x, old_arrow_x, old_arrow_y
        self.angle = math.atan2(where_y - self.rect.y, where_x - self.rect.x)  # Угол наклона
        self.vel_x = math.cos(self.angle) * self.speed  # Скорость по иксу
        self.vel_y = math.sin(self.angle) * self.speed  # Скорость по игрику
        if self.rect.x < 1500 and self.rect.y < 760:
            self.rect.x += int(self.vel_x)
            self.rect.y += int(self.vel_y)
        old_arrow_x, old_arrow_y = self.rect.x, self.rect.y

        # Если стрела вернулась к игроку, она исчезает
        if pygame.sprite.spritecollideany(self, all_sprites):
            self.kill()


# Класс босса рыцаря
class Knight(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        global where_x, where_y
        self.image = load_image("knight.png", -1)
        # Анимация ходьбы рыцаря
        self.animation_images = [load_image("knight.png", -1), load_image("knight1.png", -1),
                                 load_image("knight2.png", -1), load_image("knight3.png", -1),
                                 load_image("knight4.png", -1), load_image("knight5.png", -1),
                                 load_image("knight6.png", -1)]
        # Анимация рывка рыцаря
        self.dash_animations = [load_image("knight_attack.png", -1), load_image("knight_attack1.png", -1),
                                load_image("knight_attack2.png", -1), load_image("knight_attack3.png", -1),
                                load_image("knight_attack4.png", -1)]
        self.animation_count = 0  # Счётчик для смены изображений ходьбы
        self.speed = 2
        self.dash_count = 0  # Счётчик для смены изображений рывка
        self.can_kill = False  # Возможность убийства
        self.must_wait = False  # Нужна ли задержка после рывка
        self.dash_was = False  # Был ли рывок
        self.much_wait = 0  # Задержка (в итерациях) после рывка
        self.vel_x, self.vel_y = 0, 0
        self.rect = self.image.get_rect(center=(800, 200))
        self.angle = math.atan2(where_y - self.rect.y, where_x - self.rect.x)  # Направление движения

    def update(self):
        global where_x, where_y
        self.can_kill = False
        self.image = self.animation_images[self.animation_count // 12]  # Анимация ходьбы
        if self.animation_count + 1 == 73:
            self.animation_count = 0
        else:
            self.animation_count += 1
        # Раз в пять секунд рывок
        if int(time.time() - seconds) % 5 == 0:
            self.speed = 10
            self.dash_count += 1
            self.dash_was = False
            # Анимация рывка
            if (self.dash_count // 5) < 5:
                self.image = self.dash_animations[self.dash_count // 5]
            else:
                self.dash_count = 0
        else:
            self.speed = 2
            self.dash_count = 0
            # Без рывка рыцарь двигается за главным героем и угол движения изменяется
            self.angle = math.atan2(where_y - self.rect.y, where_x - self.rect.x)  # Угол наклона
        self.vel_x = math.cos(self.angle) * self.speed  # Скорость по иксу
        self.vel_y = math.sin(self.angle) * self.speed  # Скорость по игрику
        # Если рыцарь идёт влево, то его картинка отражается
        if self.vel_x < 0:
            self.image = pygame.transform.flip(self.image, True, False)
        if 50 < self.rect.x < 1500 and 50 < self.rect.y < 710 and self.must_wait is False:
            if 50 < (self.rect.x + int(self.vel_x)) < 1500 and 50 < (self.rect.y + int(self.vel_y)) < 710:
                self.rect.x += int(self.vel_x)
                self.rect.y += int(self.vel_y)
        # Задержка после рывка в итерациях
        elif self.must_wait is True:
            if self.much_wait == 30:
                self.must_wait = False
                self.much_wait = 0
            else:
                self.much_wait += 1
                self.can_kill = True
            self.image = load_image("dead_knight1.png", -1)
        # Проверка был ли рывок, и если рывок был, то задержка после него
        if self.speed == 2 and self.dash_was is False:
            self.must_wait = True
            self.dash_was = True
        # Убийство рыцаря
        if self.can_kill is True:
            if pygame.sprite.spritecollideany(self, arrow_group):
                self.kill()
                print('win')


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
pygame.mouse.set_visible(False)

# Создание часов(ограничителя количества кадров)
FPS = 60
clock = pygame.time.Clock()

# Состояние переката
roll = False

# Группа героя
all_sprites = pygame.sprite.Group()
sprite = pygame.sprite.Sprite()
sprite.image = pygame.transform.scale(load_image("hero.png", -1), (45, 65))

# Спрайт героя идущего налево
sprite.imageL1 = pygame.transform.scale(load_image('3.png', -1), (45, 65))
sprite.imageL2 = pygame.transform.scale(load_image('31.png', -1), (45, 65))
sprite.imageL3 = pygame.transform.scale(load_image('32.png', -1), (45, 57))
sprite.imageL4 = pygame.transform.scale(load_image('33.png', -1), (45, 68))
sprite.imageL5 = pygame.transform.scale(load_image('34.png', -1), (45, 65))

# Спрайт героя идущего вправо
sprite.imageR1 = pygame.transform.scale(load_image('4.png', -1), (50, 60))
sprite.imageR2 = pygame.transform.scale(load_image('41.png', -1), (45, 57))
sprite.imageR3 = pygame.transform.scale(load_image('42.png', -1), (50, 57))
sprite.imageR4 = pygame.transform.scale(load_image('43.png', -1), (45, 57))
sprite.imageR5 = pygame.transform.scale(load_image('44.png', -1), (50, 68))

# Спрайт героя идущего вперед
sprite.imageF1 = pygame.transform.scale(load_image('hero.png', -1), (45, 57))
sprite.imageF2 = pygame.transform.scale(load_image('hero1.png', -1), (45, 57))
sprite.imageF3 = pygame.transform.scale(load_image('hero2.png', -1), (45, 63))
sprite.imageF4 = pygame.transform.scale(load_image('hero3.png', -1), (45, 62))
sprite.imageF5 = pygame.transform.scale(load_image('hero4.png', -1), (45, 68))

# Спрайт героя идущего назад
sprite.imageB1 = pygame.transform.scale(load_image('2.png', -1), (45, 61))
sprite.imageB2 = pygame.transform.scale(load_image('21.png', -1), (45, 66))
sprite.imageB3 = pygame.transform.scale(load_image('22.png', -1), (45, 63))
sprite.imageB4 = pygame.transform.scale(load_image('23.png', -1), (45, 59))
sprite.imageB5 = pygame.transform.scale(load_image('24.png', -1), (45, 63))

# спрайт стоящего на месте игрока
sprite.stopPlayer = pygame.transform.scale(load_image('01.png', -1), (45, 61))

# спрайт идущего вверх налево
sprite.imageFL1 = pygame.transform.scale(load_image('6.png', -1), (45, 61))
sprite.imageFL2 = pygame.transform.scale(load_image('61.png', -1), (45, 61))
sprite.imageFL3 = pygame.transform.scale(load_image('62.png', -1), (45, 61))
sprite.imageFL4 = pygame.transform.scale(load_image('63.png', -1), (45, 61))
sprite.imageFL5 = pygame.transform.scale(load_image('64.png', -1), (45, 61))

# спрайт идущего вверх направо
sprite.imageFR1 = pygame.transform.scale(load_image('5.png', -1), (45, 61))
sprite.imageFR2 = pygame.transform.scale(load_image('51.png', -1), (45, 61))
sprite.imageFR3 = pygame.transform.scale(load_image('52.png', -1), (45, 61))
sprite.imageFR4 = pygame.transform.scale(load_image('53.png', -1), (45, 61))
sprite.imageFR5 = pygame.transform.scale(load_image('54.png', -1), (45, 61))

# спрайт идущего вниз налево
sprite.imageBL1 = pygame.transform.scale(load_image('7.png', -1), (45, 61))
sprite.imageBL2 = pygame.transform.scale(load_image('71.png', -1), (45, 61))
sprite.imageBL3 = pygame.transform.scale(load_image('72.png', -1), (45, 61))
sprite.imageBL4 = pygame.transform.scale(load_image('73.png', -1), (45, 61))
sprite.imageBL5 = pygame.transform.scale(load_image('74.png', -1), (45, 61))

# спрайт идущего вниз направо
sprite.imageBR1 = pygame.transform.scale(load_image('01.png', -1), (45, 61))
sprite.imageBR2 = pygame.transform.scale(load_image('12.png', -1), (45, 61))
sprite.imageBR3 = pygame.transform.scale(load_image('13.png', -1), (45, 61))
sprite.imageBR4 = pygame.transform.scale(load_image('14.png', -1), (45, 61))
sprite.imageBR5 = pygame.transform.scale(load_image('15.png', -1), (45, 61))

# спрайт перекатывающегося вправо
sprite.image_dash01 = pygame.transform.scale(load_image('dash_01.png', -1), (45, 61))
sprite.image_dash02 = pygame.transform.scale(load_image('dash_02.png', -1), (45, 61))
sprite.image_dash03 = pygame.transform.scale(load_image('dash_03.png', -1), (45, 61))
sprite.image_dash04 = pygame.transform.scale(load_image('dash_04.png', -1), (45, 61))
sprite.image_dash05 = pygame.transform.scale(load_image('dash_05.png', -1), (45, 61))
sprite.image_dash06 = pygame.transform.scale(load_image('dash_06.png', -1), (45, 61))


# Загрузка фото курсора
cursor = pygame.transform.scale(load_image("pricel1.png", -1), (20, 20))

# Размер спрайта игрока, начальные координаты и скорость
sprite.rect = sprite.image.get_rect()
where_x = sprite.rect.x = 770
where_y = sprite.rect.y = 660
hero_speed = 2
all_sprites.add(sprite)

# Группа стрелы
arrow_group = pygame.sprite.Group()

# Группа босса рыцаря
knight_group = pygame.sprite.Group()
knight_group.add(Knight())

# Счётчик времени
seconds = time.time()

# Запуск начального окна
start_screen()

# Задний фон игры
bg = load_image("1.png")

# Переменные необходимые для анимации
right, left, forward, back, forward_right, forward_left, back_right, back_left = False, False, False, False, False,\
                                                                                 False, False, False
animCount = 0

# Время последнего переката
dash_time = 0

# Проверка на то, что стрела выпущена
go_back = False

# Списки с порядками картинок для анимации
roll_Right = [sprite.image_dash01, sprite.image_dash02, sprite.image_dash03, sprite.image_dash04,
              sprite.image_dash05, sprite.image_dash06]
Right = [sprite.imageR1, sprite.imageR2, sprite.imageR3, sprite.imageR1, sprite.imageR4, sprite.imageR5]
Left = [sprite.imageL1, sprite.imageL2, sprite.imageL3, sprite.imageL1, sprite.imageL4, sprite.imageL5]
Forward = [sprite.imageF1, sprite.imageF2, sprite.imageF3, sprite.imageF1, sprite.imageF4, sprite.imageF5]
Back = [sprite.imageB1, sprite.imageB2, sprite.imageB3, sprite.imageB1, sprite.imageB4, sprite.imageB5]
FL = [sprite.imageFL1, sprite.imageFL2, sprite.imageFL3, sprite.imageFL1, sprite.imageFL4, sprite.imageFL5]
FR = [sprite.imageFR1, sprite.imageFR2, sprite.imageFR3, sprite.imageFR1, sprite.imageFR4, sprite.imageFR5]
BL = [sprite.imageBL1, sprite.imageBL2, sprite.imageBL3, sprite.imageBL1, sprite.imageBL4, sprite.imageBL5]
BR = [sprite.imageBR1, sprite.imageBR2, sprite.imageBR3, sprite.imageBR1, sprite.imageBR4, sprite.imageBR5]

# Главный игровой цикл
while running:
    hero_speed = 2
    screen.fill((255, 255, 255))
    where_x, where_y = sprite.rect.x, sprite.rect.y  # Координаты главного героя
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()

        # Выстреливание стрелы
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Если стрела не выпущена, то игрок может выстрелить
            if event.button == 1 and len(arrow_group) == 0:
                x, y = pygame.mouse.get_pos()  # Координаты курсора
                arrow_group = pygame.sprite.Group()
                arrow_group.add(Arrow(sprite.rect.x, sprite.rect.y, x, y))
                go_back = False
            # Если стрела выпущена, то она притягивается к игроку
            elif event.button == 3 and len(arrow_group) == 1:
                arrow_group = pygame.sprite.Group()
                arrow_group.add(ArrowBack(sprite.rect.x, sprite.rect.y, old_arrow_x, old_arrow_y))
                go_back = True
        # Перекат героя
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and (time.time() - dash_time) > 3:
                dash_time = time.time()
                hero_speed += 70
                roll = True

    # Перемещение персонажа
    keys = pygame.key.get_pressed()  # Список с состоянием(нажата или нет) каждой клавишы
    if keys[pygame.K_w] and keys[pygame.K_a]:
        if sprite.rect.y > 30 and sprite.rect.x > 30:
            sprite.rect.y -= hero_speed
            sprite.rect.x -= hero_speed
            where_to_go(f2=True)
    elif keys[pygame.K_w] and keys[pygame.K_d]:
        if sprite.rect.y > 30 and sprite.rect.x < 1465:
            sprite.rect.y -= hero_speed
            sprite.rect.x += hero_speed
            where_to_go(f1=True)
    elif keys[pygame.K_s] and keys[pygame.K_a]:
        if sprite.rect.y < 720 and sprite.rect.x > 30:
            sprite.rect.y += hero_speed
            sprite.rect.x -= hero_speed
            where_to_go(b2=True)
    elif keys[pygame.K_s] and keys[pygame.K_d]:
        if sprite.rect.y < 720 and sprite.rect.x < 1465:
            sprite.rect.y += hero_speed
            sprite.rect.x += hero_speed
            where_to_go(b1=True)
    elif keys[pygame.K_a]:
        if sprite.rect.x > 30:
            sprite.rect.x -= hero_speed
            where_to_go(go_left=True)
    elif keys[pygame.K_d]:
        if sprite.rect.x < 1465:
            sprite.rect.x += hero_speed
            where_to_go(go_right=True)
    elif keys[pygame.K_w]:
        if sprite.rect.y > 30:
            sprite.rect.y -= hero_speed
            where_to_go(go_forward=True)
    elif keys[pygame.K_s]:
        if sprite.rect.y < 720:
            sprite.rect.y += hero_speed
            where_to_go(go_back=True)
    else:
        where_to_go()
        animCount = 0
    # Если рыцарь задел героя, то игра проиграна
    if pygame.sprite.spritecollideany(sprite, knight_group):
        print("lose")
    screen.blit(bg, (0, 0))  # Задний фон
    all_sprites.draw(screen)  # Отрисовка героя
    draw_player()  # Отрисовка анимации героя
    arrow_group.draw(screen)  # Отрисовка стрела
    knight_group.draw(screen)  # Отрисовка рыцаря
    # Если стрела выпущена, то она будет возвращаться только если зажата правая кнопка мыши
    if go_back is True:
        if pygame.mouse.get_pressed()[2]:
            arrow_group.update()
    else:
        arrow_group.update()
    # Замена курсора
    if pygame.mouse.get_focused():
        screen.blit(cursor, pygame.mouse.get_pos())
    knight_group.update()
    pygame.display.flip()  # Обновление кадра
    pygame.display.update()
    clock.tick(FPS)  # Ограничение частоты кадров
