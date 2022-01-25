import math
import os
import sys
import pygame
import time
import datetime


# Функция добавления текста на экран
def print_text(message, xx, yy, font_color=(255, 255, 255), font_type=None, font_size=30):
    font_type = pygame.font.Font(font_type, font_size)  # Шрифт
    text = font_type.render(message, True, font_color)  # Текст
    screen.blit(text, (xx, yy))  # Добавление на экран


# Функция определения направления движения персонажа
def where_to_go(go_left=False, go_right=False, go_forward=False, back1=False, f1=False, f2=False, b1=False, b2=False):
    global left, right, forward, back, forward_right, forward_left, back_right, back_left
    left = go_left
    right = go_right
    forward = go_forward
    back = back1
    forward_right = f1
    forward_left = f2
    back_right = b1
    back_left = b2


# Экран победы
def win_screen():
    global attempt_time, attempts  # Время попытки из главного цикла и количество попыток
    # Лучшее время прохождения, считанное из файла
    best_time_file = open('data/best_time.txt', 'r')
    time_from_file = best_time_file.read().split(":")

    temp_time = attempt_time.split(":")  # Временная локальная переменная, хранящая время попытки в виде списка
    beated = False  # Побит ли рекорд

    # Перевод времени попыток в секунды для сравнения
    seconds_from_file = (int(time_from_file[0]) * 3600 + int(time_from_file[1]) * 60 + int(time_from_file[2]))
    seconds_from_attempt = (int(temp_time[0]) * 3600 + int(temp_time[1]) * 60 + int(temp_time[2]))

    # Сравнение времени прохождения, и если лучшее время побито, то оно записывается в файл с лучшим временем
    if seconds_from_attempt < seconds_from_file:
        file = open('data/best_time.txt', 'w')
        file.write(attempt_time)
        beated = True

    fon = pygame.transform.scale(load_image('win_screen.png'), (width, height))  # Фон
    while True:
        screen.blit(fon, (0, 0))  # Заполнение фона начального экрана
        # Если рекорд побит, то добавляется соответсвующая надпись
        if beated is True:
            print_text(f'Вы побили свой рекорд!', 650, 320)
        print_text(f'Время вашей попытки: {attempt_time}', 5, 7)  # Текст с временем попытки
        # Текст с количеством попыток, затраченных на прохождение
        print_text(f'На прохождение ушло {attempts} попыток', 5, 40)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Проверка нажатия на кнопку EXIT
                if 617 < event.pos[0] < 918 and 358 < event.pos[1] < 439:
                    terminate()  # Окончание работы
        # Замена курсора
        if pygame.mouse.get_focused():
            screen.blit(cursor, pygame.mouse.get_pos())
        pygame.display.flip()
        clock.tick(FPS)


# Функция проигрыша (смерти героя)
def lose_screen():
    global attempt_time, death_sound  # Время попытки из главного цикла и звук смерти

    # Проигрывание звука смерти
    death_sound.play()

    fon = pygame.transform.scale(load_image('lose_screen.png'), (width, height))  # Фон
    while True:
        screen.blit(fon, (0, 0))  # Заполнение фона начального экрана
        print_text(f'Время вашей попытки: {attempt_time}', 5, 7)  # Текст с временем попытки
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Проверка нажатия на кнопку Try again
                if 632 < event.pos[0] < 947 and 364 < event.pos[1] < 440:
                    restart_level()  # Перезапуск уровня
                    return attempt_start_time * -1  # Сброс времени
                # Проверка нажатия на кнопку EXIT
                elif 634 < event.pos[0] < 938 and 475 < event.pos[1] < 557:
                    terminate()  # Окончание работы
        # Замена курсора
        if pygame.mouse.get_focused():
            screen.blit(cursor, pygame.mouse.get_pos())
        pygame.display.flip()
        clock.tick(FPS)


# Функция отрисовки персонажа
def draw_player():
    global animCount, roll, win_status
    if animCount + 1 >= 73 and win_status is False:
        animCount = 0
        roll = False
    elif animCount + 1 >= 130:  # В анимации танца больше картинок, поэтому счётчик до большего числа
        animCount = 0
    # Анимация танца
    if win_status:
        sprite.image = Win[animCount // 12]
    # Анимация идущего или перекатывающегося влево
    elif left:
        if roll is True:
            sprite.image = roll_Left[animCount // 12]
        else:
            sprite.image = Left[animCount // 12]
    # Анимация идущего или перекатывающегося вправо
    elif right:
        if roll is True:
            sprite.image = roll_Right[animCount // 12]
        else:
            sprite.image = Right[animCount // 12]
    # Анимация идущего или перекатывающегося вверх
    elif forward:
        if roll is True:
            sprite.image = roll_Forward[animCount // 12]
        else:
            sprite.image = Forward[animCount // 12]
    # Анимация идущего или перекатывающегося вниз
    elif back:
        if roll is True:
            sprite.image = roll_Back[animCount // 12]
        else:
            sprite.image = Back[animCount // 12]
    # Анимация идущего или перекатывающегося вправо вверх
    elif forward_right:
        if roll is True:
            sprite.image = roll_FR[animCount // 12]
        else:
            sprite.image = FR[animCount // 12]
    # Анимация идущего или перекатывающегося влево вверх
    elif forward_left:
        if roll is True:
            sprite.image = roll_FL[animCount // 12]
        else:
            sprite.image = FL[animCount // 12]
    # Анимация идущего или перекатывающегося влево вниз
    elif back_left:
        if roll is True:
            sprite.image = roll_BL[animCount // 12]
        else:
            sprite.image = BL[animCount // 12]
    # Анимация идущего или перекатывающегося вправо вниз
    elif back_right:
        if roll is True:
            sprite.image = roll_BR[animCount // 12]
        else:
            sprite.image = BR[animCount // 12]
    else:
        sprite.image = sprite.stopPlayer
    animCount += 1


# Функция паузы
def pause():
    pause_time = time.time()  # Время начала паузы
    paused = True
    print_text('Нажмите Enter для продолжения или R для рестарта', 520, 385)  # Добавление текста на экран
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        keys = pygame.key.get_pressed()
        # Проверка нажатия на кнопку ENTER (продолжение игры)
        if keys[pygame.K_RETURN]:
            paused = False
        # Если нажата R, то рестарт
        elif keys[pygame.K_r]:
            restart_level()
            return attempt_start_time * -1  # Чтобы время стало отрицательным
        pygame.display.update()
        clock.tick(15)
    pause_time = time.time() - pause_time
    return pause_time  # Возвращение времени (в секундах), затраченного на паузу


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


# Функция рестарта
def restart_level():
    global where_x, where_y, arrow_group, boss_group, attempt_start_time, animCount, roll, Level, Golem_attack_group
    global Crystal_attack_group, attempts
    # Обновление координат
    where_x = sprite.rect.x = 770
    where_y = sprite.rect.y = 660
    # Создание босса заново
    boss_group.empty()
    boss_group.add(Knight())
    Golem_attack_group.empty()
    Crystal_attack_group.empty()
    Level = 1
    attempts += 1

    # Обновление анимации
    animCount = 0
    roll = False
    attempt_start_time = time.time()  # Обнуление времени
    arrow_group.empty()  # Обновление стрел


# Начальное окно
def start_screen():
    fon = pygame.transform.scale(load_image('fon.png'), (width, height))

    best_time_file = open('data/best_time.txt', 'r').read()  # Лучшее время прохождения (считано из файла)

    while True:
        screen.blit(fon, (0, 0))
        print_text(f'Ваш рекорд: {best_time_file}', 5, 7)  # Добавление лучшего времени прохождения на экран
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Проверка нажатия на кнопку START
                if 644 < event.pos[0] < 933 and 296 < event.pos[1] < 371:
                    start_sound.play()  # Звук начала игры
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
        self.image = load_image("arrow.png", -1)  # Картинка стрелы
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
        if pygame.sprite.collide_mask(self, sprite):
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
        self.animation_count = 0  # Счётчик для смены изображений
        self.speed = 2
        self.dash_count = 0  # Счётчик для смены изображений рывка
        self.can_kill = False  # Возможность убийства
        self.must_wait = False  # Нужна ли задержка после рывка
        self.dash_was = False  # Был ли рывок
        self.much_wait = 0  # Задержка (в итерациях) после рывка
        self.vel_x, self.vel_y = 0, 0
        self.rect = self.image.get_rect(center=(780, 300))
        self.angle = math.atan2(where_y - self.rect.y, where_x - self.rect.x)  # Направление движения

    def update(self):
        global where_x, where_y, win_status

        self.can_kill = False  # Статус возможности убить босса героем
        self.image = self.animation_images[self.animation_count // 12]  # Анимация ходьбы
        if self.animation_count + 1 == 73:
            self.animation_count = 0  # Начало анимации заново
        else:
            self.animation_count += 1  # Смена картинок анимации

        # Раз в три секунд рывок
        if int(time.time() - seconds) % 3 == 0:
            self.speed = 10
            self.dash_count += 1
            self.dash_was = False
            # Анимация рывка
            if (self.dash_count // 5) < 5:
                self.image = self.dash_animations[self.dash_count // 5]
            else:
                self.dash_count = 0
        else:
            # Без рывка рыцарь двигается за главным героем и угол движения изменяется, а скорость становится обычной
            self.speed = 2
            self.dash_count = 0
            self.angle = math.atan2(where_y - self.rect.y, where_x - self.rect.x)  # Угол движения

        self.vel_x = math.cos(self.angle) * self.speed  # Скорость по иксу
        self.vel_y = math.sin(self.angle) * self.speed  # Скорость по игрику

        # Если рыцарь идёт влево, то его картинка отражается
        if self.vel_x < 0:
            self.image = pygame.transform.flip(self.image, True, False)
        if 59 < self.rect.x < 1440 and 100 < self.rect.y < 530 and self.must_wait is False:
            if 59 < (self.rect.x + int(self.vel_x)) < 1440 and 100 < (self.rect.y + int(self.vel_y)) < 530:
                self.rect.x += int(self.vel_x)
                self.rect.y += int(self.vel_y)

        # Задержка после рывка в итерациях
        elif self.must_wait is True:
            if self.much_wait == 20:
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
                win_status = True  # Анимация танца
                self.kill()

        # Если босс задел героя, то игра проиграна
        if pygame.sprite.collide_mask(sprite, self):
            lose_screen()  # Запуск экрана проигрыша


# Класс босса голема
class Golem(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image("golem.png", -1)
        # Анимация ходьбы голема
        self.animation_images = [pygame.transform.scale(load_image("golem.png", -1), (250, 238)),
                                 pygame.transform.scale(load_image("golem1.png", -1), (250, 238)),
                                 pygame.transform.scale(load_image("golem2.png", -1), (250, 238)),
                                 pygame.transform.scale(load_image("golem3.png", -1), (250, 238))]
        # Анимация стрельбы
        self.shoot_images = [pygame.transform.scale(load_image("golem4.png", -1), (250, 238)),
                             pygame.transform.scale(load_image("golem5.png", -1), (250, 238)),
                             pygame.transform.scale(load_image("golem6.png", -1), (250, 238)),
                             pygame.transform.scale(load_image("golem7.png", -1), (250, 238)),
                             pygame.transform.scale(load_image("golem8.png", -1), (250, 238)),
                             pygame.transform.scale(load_image("golem9.png", -1), (250, 238)),
                             pygame.transform.scale(load_image("golem10.png", -1), (250, 238)),
                             pygame.transform.scale(load_image("golem11.png", -1), (250, 238)),
                             pygame.transform.scale(load_image("golem12.png", -1), (250, 238))]
        # Анимация пульсации
        self.pulse_images = [pygame.transform.scale(load_image("golem13.png", -1), (250, 238)),
                             pygame.transform.scale(load_image("golem14.png", -1), (250, 238)),
                             pygame.transform.scale(load_image("golem15.png", -1), (250, 238)),
                             pygame.transform.scale(load_image("golem16.png", -1), (250, 238)),
                             pygame.transform.scale(load_image("golem17.png", -1), (250, 238)),
                             pygame.transform.scale(load_image("golem18.png", -1), (250, 238)),
                             pygame.transform.scale(load_image("golem19.png", -1), (250, 238)),
                             pygame.transform.scale(load_image("golem20.png", -1), (250, 238))]
        self.pulse_time = time.time()  # Время последней пульсации, во время которой можно убить голема
        self.pulse_count = 0  # Счётчик для анимации пульсации
        # Анимация возможности убийства
        self.can_kill_images = []
        self.shoot_count = 0  # Счётчик для смены изображений стрельбы
        self.animation_count = 0  # Счётчик для смены изображений
        self.rect = self.image.get_rect(center=(800, 170))
        self.vel_x, self.vel_y = 0, 0  # Скорость по оси x и оси y
        self.angle = math.atan2(where_y - self.rect.y, where_x - self.rect.x)  # Направление движения
        self.speed = 1.5  # Скорость голема
        self.shoot_iterations = 0  # Счётчик итераций для стрельбы

    def update(self):
        global win_status

        # Раз в пять секунд пусьлация
        if (time.time() - self.pulse_time) > 5:
            self.pulse_time = time.time()
            self.pulse_count += 1

        # Анимация пульсации, во время которой голема можно убить
        if self.pulse_count != 0:
            self.image = self.pulse_images[self.pulse_count]  # Анимация пульсация
            # Если во время пульсации попасть голему в глаз, то он умирает
            if pygame.sprite.spritecollideany(self, arrow_group):
                for i in arrow_group:
                    if self.rect.x + 50 < i.rect.x < self.rect.x + 195 and self.rect.y < i.rect.y < self.rect.y + 100:
                        win_status = True
                        self.kill()
            if self.pulse_count + 1 == 8:
                self.pulse_count = 0
            else:
                self.pulse_count += 1

        # Анимация стрельбы
        elif self.shoot_count != 0:
            self.image = self.shoot_images[self.shoot_count // 2]
            if self.shoot_count + 1 == 18:
                self.shoot_count = 0
            else:
                self.shoot_count += 1

        # Анимация ходьбы
        else:
            self.image = self.animation_images[self.animation_count // 12]
            if self.animation_count + 1 == 43:
                self.animation_count = 0  # Начало анимации заново
            else:
                self.animation_count += 1  # Смена картинок анимации

        # Раз в 30 итераций выстрел
        if self.shoot_iterations == 30:
            self.shoot_count += 1
            # Смещенение снаряда голема если он идёт влево, чтобы выглядело так, что он стреляет из руки
            if self.vel_x > 0:
                Golem_attack_group.add(GolemAttack(where_x, where_y, self.rect.x + 270, self.rect.y))
            else:
                Golem_attack_group.add(GolemAttack(where_x, where_y, self.rect.x, self.rect.y))
            self.shoot_iterations = 0
        else:
            self.shoot_iterations += 1

        # Разворот картинки если голем идёт влево
        if self.vel_x < 0:
            self.image = pygame.transform.flip(self.image, True, False)

        self.angle = math.atan2(where_y - self.rect.y, where_x - self.rect.x)  # Угол движения (направление)
        self.vel_x = math.cos(self.angle) * self.speed  # Скорость по иксу
        self.vel_y = math.sin(self.angle) * self.speed  # Скорость по игрику

        # Перемещение
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        # Если босс задел героя, то игра проиграна
        if pygame.sprite.collide_mask(sprite, self):
            lose_screen()  # Запуск экрана проигрыша


# Класс снарядов голема
class GolemAttack(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, old_x, old_y):
        super().__init__()
        self.image = pygame.transform.scale(load_image("golem_shoot.png", -1), (100, 40))
        self.rect = self.image.get_rect(center=(old_x, old_y))
        self.speed = 5  # Начальная скорость
        self.angle = math.atan2(pos_y - self.rect.y, pos_x - self.rect.x)  # Угол наклона
        self.vel_x = math.cos(self.angle) * self.speed  # Скорость по иксу
        self.vel_y = math.sin(self.angle) * self.speed  # Скорость по игрику

        # Угол поворота картинки снаряда и разворачивание его в направлени выпускания
        rel_x, rel_y = old_x - pos_x, old_y - pos_y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.image = pygame.transform.rotate(self.image, angle)

    def update(self):
        self.vel_x = math.cos(self.angle) * self.speed  # Скорость по иксу
        self.vel_y = math.sin(self.angle) * self.speed  # Скорость по игрику
        if self.rect.x < 1500 and self.rect.y < 760:
            self.rect.x += int(self.vel_x)
            self.rect.y += int(self.vel_y)
        else:
            self.kill()

        # Если снаряд задел героя, то игра проиграна
        if pygame.sprite.collide_mask(sprite, self):
            lose_screen()  # Запуск экрана проигрыша


# Класс босса кристала
class Crystal(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Цвет заднего фона и загрузка изображения кристалла с убраным задним фоном
        color = (127, 146, 255)
        self.image = pygame.transform.scale(load_image("crystal.png", color), (100, 240))

        # Обычная анимация кристалла
        self.animation_images = [pygame.transform.scale(load_image("crystal.png", color), (100, 240)),
                                 pygame.transform.scale(load_image("crystal1.png", color), (100, 240)),
                                 pygame.transform.scale(load_image("crystal2.png", color), (100, 240)),
                                 pygame.transform.scale(load_image("crystal3.png", color), (100, 240)),
                                 pygame.transform.scale(load_image("crystal4.png", color), (100, 240)),
                                 pygame.transform.scale(load_image("crystal5.png", color), (100, 240))]
        # Анимация стрельбы
        self.shoot_images = [pygame.transform.scale(load_image("crystal6.png", color), (100, 240)),
                             pygame.transform.scale(load_image("crystal7.png", color), (100, 240)),
                             pygame.transform.scale(load_image("crystal8.png", color), (100, 240))]

        # Время появления босса
        self.creation_time = time.time()
        self.shoot_count = 0  # Счётчик для анимации стрельбы
        self.animation_count = 0  # Счётчик для обычной анимации
        self.shoot_time = time.time()  # Время последнего выстрела
        self.rect = self.image.get_rect(center=(800, 300))

    def update(self):
        global Crystal_attack_group, win_status
        # Каждые две секунды выстрел
        if (time.time() - self.shoot_time) > 0.5:
            Crystal_attack_group.add(CrystalAttack(self.rect.x, self.rect.y))
            self.shoot_time = time.time()
            self.shoot_count += 1

        # Анимация выстрелов
        if self.shoot_count != 0:
            self.image = self.shoot_images[self.shoot_count // 6]
            if self.shoot_count + 1 == 18:
                self.shoot_count = 0
            else:
                self.shoot_count += 1

            # Во время выстрела кристал можно убить, если с момента создания босса прошло больше трёх
            if pygame.sprite.spritecollideany(self, arrow_group) and (time.time() - self.creation_time) > 3:
                win_status = True  # Анимация танца
                self.kill()

        # Обычная анимация
        else:
            self.image = self.animation_images[self.animation_count // 6]
            if self.animation_count + 1 == 34:
                self.animation_count = 0  # Начало анимации заново
            else:
                self.animation_count += 1  # Смена картинок анимации

        # Если босс задел героя, то игра проиграна
        if pygame.sprite.collide_mask(sprite, self):
            lose_screen()  # Запуск экрана проигрыша


# Класс лазеров кристала
class CrystalAttack(pygame.sprite.Sprite):
    def __init__(self, crystal_x, crystal_y):
        super().__init__()
        self.image = pygame.transform.scale(load_image("laser.png", (116, 154, 212)), (100, 69))
        self.speed = 6  # Начальная скорость
        self.vel_x = self.vel_y = 0  # Скорость по оси икс и игрик
        self.rect = self.image.get_rect(center=(crystal_x + 60, crystal_y + 10))
        self.angle = math.atan2(where_y - self.rect.y, where_x - self.rect.x)  # Угол наклона (направление)

        # Угол поворота картинки снаряда и разворачивание его в направлени выпускания
        rel_x, rel_y = crystal_x + 60 - where_x, crystal_y + 10 - where_y
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.image = pygame.transform.rotate(self.image, angle)

    def update(self):
        self.angle = math.atan2(where_y - self.rect.y, where_x - self.rect.x)  # Угол наклона (направление)
        self.vel_x = math.cos(self.angle) * self.speed  # Скорость по иксу
        self.vel_y = math.sin(self.angle) * self.speed  # Скорость по игрику
        if self.rect.x < 1500 and self.rect.y < 760:
            self.rect.x += int(self.vel_x)
            self.rect.y += int(self.vel_y)
        else:
            self.kill()

        # Если снаряд задел героя, то игра проиграна
        if pygame.sprite.collide_mask(sprite, self):
            lose_screen()  # Запуск экрана проигрыша

        # Если стрела попала в снаряд, он взрывается и исчезает, а стрела возвращается назад
        if pygame.sprite.spritecollideany(self, arrow_group):
            self.kill()
            arrow_group.empty()


# Инициализация пайгейма
pygame.init()

# Загрузка музыки и её воспроизведение
pygame.mixer.music.load("data/menu.ogg")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

arrow_sound = pygame.mixer.Sound("data/arrow_shoot.ogg")  # Звук выстрела
death_sound = pygame.mixer.Sound("data/death.ogg")  # Звук смерти главного героя
start_sound = pygame.mixer.Sound("data/StartGame.ogg")  # Звук начала игры

# Группа снарядов босса голема
Golem_attack_group = pygame.sprite.Group()

# Группа лазеров босса кристала
Crystal_attack_group = pygame.sprite.Group()

# Создание главного окна
size = width, height = 1530, 790
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Dungeon Master')
running = True
pygame.mouse.set_visible(False)

# Создание часов(ограничителя количества кадров)
FPS = 60
clock = pygame.time.Clock()

# Уровень
Level = 1

# Состояние переката
roll = False

# Группа героя
hero_group = pygame.sprite.Group()
sprite = pygame.sprite.Sprite()
sprite.image = pygame.transform.scale(load_image("hero.png", -1), (45, 65))

# Спрайт танцующего
sprite.image_win1 = pygame.transform.scale(load_image('win.png', -1), (45, 65))
sprite.image_win2 = pygame.transform.scale(load_image('win1.png', -1), (45, 65))
sprite.image_win3 = pygame.transform.scale(load_image('win2.png', -1), (45, 57))
sprite.image_win4 = pygame.transform.scale(load_image('win3.png', -1), (45, 68))
sprite.image_win5 = pygame.transform.scale(load_image('win4.png', -1), (45, 65))
sprite.image_win6 = pygame.transform.scale(load_image('win5.png', -1), (45, 65))
sprite.image_win7 = pygame.transform.scale(load_image('win6.png', -1), (45, 65))
sprite.image_win8 = pygame.transform.scale(load_image('win7.png', -1), (45, 57))
sprite.image_win9 = pygame.transform.scale(load_image('win8.png', -1), (45, 68))
sprite.image_win10 = pygame.transform.scale(load_image('win9.png', -1), (45, 65))
sprite.image_win11 = pygame.transform.scale(load_image('win10.png', -1), (45, 65))

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

# Спрайт героя идущего вверх
sprite.imageF1 = pygame.transform.scale(load_image('hero.png', -1), (45, 57))
sprite.imageF2 = pygame.transform.scale(load_image('hero1.png', -1), (45, 57))
sprite.imageF3 = pygame.transform.scale(load_image('hero2.png', -1), (45, 63))
sprite.imageF4 = pygame.transform.scale(load_image('hero3.png', -1), (45, 62))
sprite.imageF5 = pygame.transform.scale(load_image('hero4.png', -1), (45, 68))

# Спрайт героя идущего вниз
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

# спрайт перекатываюшегося вверх
sprite.image_dash10 = pygame.transform.scale(load_image('dash_10.png', -1), (45, 61))
sprite.image_dash11 = pygame.transform.scale(load_image('dash_11.png', -1), (45, 61))
sprite.image_dash12 = pygame.transform.scale(load_image('dash_12.png', -1), (45, 61))
sprite.image_dash13 = pygame.transform.scale(load_image('dash_13.png', -1), (45, 61))
sprite.image_dash14 = pygame.transform.scale(load_image('dash_14.png', -1), (45, 61))
sprite.image_dash15 = pygame.transform.scale(load_image('dash_15.png', -1), (45, 61))

# спрайт перекатываюшегося влево
sprite.image_dash20 = pygame.transform.scale(load_image('dash_20.png', -1), (45, 61))
sprite.image_dash21 = pygame.transform.scale(load_image('dash_21.png', -1), (45, 61))
sprite.image_dash22 = pygame.transform.scale(load_image('dash_22.png', -1), (45, 61))
sprite.image_dash23 = pygame.transform.scale(load_image('dash_23.png', -1), (45, 61))
sprite.image_dash24 = pygame.transform.scale(load_image('dash_24.png', -1), (45, 61))
sprite.image_dash25 = pygame.transform.scale(load_image('dash_25.png', -1), (45, 61))

# спрайт перекатываюшегося вниз
sprite.image_dash30 = pygame.transform.scale(load_image('dash_30.png', -1), (45, 61))
sprite.image_dash31 = pygame.transform.scale(load_image('dash_31.png', -1), (45, 61))
sprite.image_dash32 = pygame.transform.scale(load_image('dash_32.png', -1), (45, 61))
sprite.image_dash33 = pygame.transform.scale(load_image('dash_33.png', -1), (45, 61))
sprite.image_dash34 = pygame.transform.scale(load_image('dash_34.png', -1), (45, 61))
sprite.image_dash35 = pygame.transform.scale(load_image('dash_35.png', -1), (45, 61))

# спрайт перекатываюшегося вниз направо
sprite.image_dash40 = pygame.transform.scale(load_image('dash_40.png', -1), (45, 61))
sprite.image_dash41 = pygame.transform.scale(load_image('dash_41.png', -1), (45, 61))
sprite.image_dash42 = pygame.transform.scale(load_image('dash_42.png', -1), (45, 61))
sprite.image_dash43 = pygame.transform.scale(load_image('dash_43.png', -1), (45, 61))
sprite.image_dash44 = pygame.transform.scale(load_image('dash_44.png', -1), (45, 61))
sprite.image_dash45 = pygame.transform.scale(load_image('dash_45.png', -1), (45, 61))

# спрайт перекатываюшегося вниз влево
sprite.image_dash50 = pygame.transform.scale(load_image('dash_50.png', -1), (45, 61))
sprite.image_dash51 = pygame.transform.scale(load_image('dash_51.png', -1), (45, 61))
sprite.image_dash52 = pygame.transform.scale(load_image('dash_52.png', -1), (45, 61))
sprite.image_dash53 = pygame.transform.scale(load_image('dash_53.png', -1), (45, 61))
sprite.image_dash54 = pygame.transform.scale(load_image('dash_54.png', -1), (45, 61))
sprite.image_dash55 = pygame.transform.scale(load_image('dash_55.png', -1), (45, 61))

# спрайт перекатываюшегося вверх влево
sprite.image_dash70 = pygame.transform.scale(load_image('dash_70.png', -1), (45, 61))
sprite.image_dash71 = pygame.transform.scale(load_image('dash_71.png', -1), (45, 61))
sprite.image_dash72 = pygame.transform.scale(load_image('dash_72.png', -1), (45, 61))
sprite.image_dash73 = pygame.transform.scale(load_image('dash_73.png', -1), (45, 61))
sprite.image_dash74 = pygame.transform.scale(load_image('dash_74.png', -1), (45, 61))
sprite.image_dash75 = pygame.transform.scale(load_image('dash_75.png', -1), (45, 61))

# спрайт перекатываюшегося вверх вправо
sprite.image_dash80 = pygame.transform.scale(load_image('dash_80.png', -1), (45, 61))
sprite.image_dash81 = pygame.transform.scale(load_image('dash_81.png', -1), (45, 61))
sprite.image_dash82 = pygame.transform.scale(load_image('dash_82.png', -1), (45, 61))
sprite.image_dash83 = pygame.transform.scale(load_image('dash_83.png', -1), (45, 61))
sprite.image_dash84 = pygame.transform.scale(load_image('dash_84.png', -1), (45, 61))
sprite.image_dash85 = pygame.transform.scale(load_image('dash_85.png', -1), (45, 61))


# Загрузка фото курсора
cursor = pygame.transform.scale(load_image("pricel1.png"), (20, 20))

# Размер спрайта игрока, начальные координаты и скорость
sprite.rect = sprite.image.get_rect()
where_x = sprite.rect.x = 770
where_y = sprite.rect.y = 660
hero_speed = 2
hero_group.add(sprite)

# Группа стрелы
arrow_group = pygame.sprite.Group()

# Счётчик попыток
attempts = 1

# Запуск начального окна
start_screen()

# Группа босса
boss_group = pygame.sprite.Group()
boss_group.add(Knight())

# Счётчик времени
seconds = time.time()

# Время начала прохождения
attempt_start_time = time.time()

# Задний фон игры
bg = load_image("bg_test.png")

# Переменные необходимые для анимации
right, left, forward, back, forward_right, forward_left, back_right, back_left = False, False, False, False, False,\
                                                                                 False, False, False
animCount = 0

# Проверка на победу игрока
win_status = False

# Время последнего переката
dash_time = 0

# Проверка на то, что стрела выпущена
go_back = False

# Списки с порядками картинок для анимации
roll_Right = [sprite.image_dash01, sprite.image_dash02, sprite.image_dash03, sprite.image_dash04,
              sprite.image_dash05, sprite.image_dash06]
roll_Forward = [sprite.image_dash10, sprite.image_dash11, sprite.image_dash12, sprite.image_dash13,
                sprite.image_dash14, sprite.image_dash15]
roll_Left = [sprite.image_dash20, sprite.image_dash21, sprite.image_dash22, sprite.image_dash23,
             sprite.image_dash24, sprite.image_dash25]
roll_Back = [sprite.image_dash30, sprite.image_dash31, sprite.image_dash32, sprite.image_dash33,
             sprite.image_dash34, sprite.image_dash35]
roll_BR = [sprite.image_dash40, sprite.image_dash41, sprite.image_dash42, sprite.image_dash43,
           sprite.image_dash44, sprite.image_dash45]
roll_BL = [sprite.image_dash50, sprite.image_dash51, sprite.image_dash52, sprite.image_dash53,
           sprite.image_dash54, sprite.image_dash55]
roll_FL = [sprite.image_dash70, sprite.image_dash71, sprite.image_dash72, sprite.image_dash73,
           sprite.image_dash74, sprite.image_dash75]
roll_FR = [sprite.image_dash80, sprite.image_dash81, sprite.image_dash82, sprite.image_dash83,
           sprite.image_dash84, sprite.image_dash85]
Right = [sprite.imageR1, sprite.imageR2, sprite.imageR3, sprite.imageR1, sprite.imageR4, sprite.imageR5]
Left = [sprite.imageL1, sprite.imageL2, sprite.imageL3, sprite.imageL1, sprite.imageL4, sprite.imageL5]
Forward = [sprite.imageF1, sprite.imageF2, sprite.imageF3, sprite.imageF1, sprite.imageF4, sprite.imageF5]
Back = [sprite.imageB1, sprite.imageB2, sprite.imageB3, sprite.imageB1, sprite.imageB4, sprite.imageB5]
FL = [sprite.imageFL1, sprite.imageFL2, sprite.imageFL3, sprite.imageFL1, sprite.imageFL4, sprite.imageFL5]
FR = [sprite.imageFR1, sprite.imageFR2, sprite.imageFR3, sprite.imageFR1, sprite.imageFR4, sprite.imageFR5]
BL = [sprite.imageBL1, sprite.imageBL2, sprite.imageBL3, sprite.imageBL1, sprite.imageBL4, sprite.imageBL5]
BR = [sprite.imageBR1, sprite.imageBR2, sprite.imageBR3, sprite.imageBR1, sprite.imageBR4, sprite.imageBR5]
Win = [sprite.image_win1, sprite.image_win2, sprite.image_win3, sprite.image_win4, sprite.image_win5, sprite.image_win6,
       sprite.image_win7, sprite.image_win8, sprite.image_win9, sprite.image_win10, sprite.image_win11]

# Главный игровой цикл
while running:
    attempt_time = int(time.time() - attempt_start_time)  # Время попытки
    attempt_time = str(datetime.timedelta(seconds=attempt_time))  # Время попытки в часах, минутах и секундах

    hero_speed = 2  # Скорость персонажа
    where_x, where_y = sprite.rect.x, sprite.rect.y  # Координаты главного героя

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()

        # Выстреливание стрелы
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Если стрела не выпущена, то игрок может выстрелить
            if event.button == 1 and len(arrow_group) == 0:
                arrow_sound.play()
                x, y = pygame.mouse.get_pos()  # Координаты курсора
                arrow_group.empty()
                arrow_group.add(Arrow(sprite.rect.x, sprite.rect.y, x, y))
                go_back = False
            # Если стрела выпущена, то она притягивается к игроку
            elif event.button == 3 and len(arrow_group) == 1:
                arrow_group.empty()
                arrow_group.add(ArrowBack(sprite.rect.x, sprite.rect.y, old_arrow_x, old_arrow_y))
                go_back = True

        # Перекат героя
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and (time.time() - dash_time) > 1:
                dash_time = time.time()  # Время последнего переката
                hero_speed += 70
                roll = True

    # Перемещение персонажа
    keys = pygame.key.get_pressed()  # Список с состоянием(нажата или нет) каждой клавишы
    # Перемещение влево вверх
    if keys[pygame.K_w] and keys[pygame.K_a]:
        if sprite.rect.y > 200 and sprite.rect.x > 60:
            sprite.rect.y -= hero_speed
            sprite.rect.x -= hero_speed
            where_to_go(f2=True)
    # Перемещение вправо вверх
    elif keys[pygame.K_w] and keys[pygame.K_d]:
        if sprite.rect.y > 200 and sprite.rect.x < 1465:
            sprite.rect.y -= hero_speed
            sprite.rect.x += hero_speed
            where_to_go(f1=True)
    # Перемещение влево вниз
    elif keys[pygame.K_s] and keys[pygame.K_a]:
        if sprite.rect.y < 680 and sprite.rect.x > 60:
            sprite.rect.y += hero_speed
            sprite.rect.x -= hero_speed
            where_to_go(b2=True)
    # Перемещение вправо вниз
    elif keys[pygame.K_s] and keys[pygame.K_d]:
        if sprite.rect.y < 680 and sprite.rect.x < 1465:
            sprite.rect.y += hero_speed
            sprite.rect.x += hero_speed
            where_to_go(b1=True)
    # Перемещение влево
    elif keys[pygame.K_a]:
        if sprite.rect.x > 60:
            sprite.rect.x -= hero_speed
            where_to_go(go_left=True)
    # Перемещение вправо
    elif keys[pygame.K_d]:
        if sprite.rect.x < 1465:
            sprite.rect.x += hero_speed
            where_to_go(go_right=True)
    # Перемещение вверх
    elif keys[pygame.K_w]:
        if sprite.rect.y > 200:
            sprite.rect.y -= hero_speed
            where_to_go(go_forward=True)
    # Перемещение вниз
    elif keys[pygame.K_s]:
        if sprite.rect.y < 680:
            sprite.rect.y += hero_speed
            where_to_go(back1=True)
    # Если игрок не победил, то будет картинка стоящего на месте героя
    elif win_status is False:
        where_to_go()
        animCount = 0

    # Если нажат ESCAPE - пауза
    if keys[pygame.K_ESCAPE]:
        attempt_start_time += int(pause())  # Время затраченное на паузу не идёт в счёт времени затраченного на попытку
        if attempt_start_time < 0:  # Если был рестарт, то время сбрасывается
            attempt_start_time = time.time()

    # Если стрела выпущена, то она будет возвращаться только если зажата правая кнопка мыши
    if go_back is True:
        if pygame.mouse.get_pressed()[2]:
            arrow_group.update()  # Обновление стрелы
    else:
        arrow_group.update()  # Обновление стрелы

    boss_group.update()  # Обновление босса
    screen.blit(bg, (0, 0))  # Задний фон
    print_text(attempt_time, 10, 10)  # Время попытки
    draw_player()  # Анимации героя (изменение его картинок)
    hero_group.draw(screen)  # Отрисовка героя
    arrow_group.draw(screen)  # Отрисовка стрелы
    boss_group.draw(screen)  # Отрисовка босса

    # Если второй уровень, то обновление и отрисовка снарядов голема
    if Level == 2:
        Golem_attack_group.update()
        Golem_attack_group.draw(screen)

    if Level == 3:
        Crystal_attack_group.update()
        Crystal_attack_group.draw(screen)

    # Замена курсора
    if pygame.mouse.get_focused():
        screen.blit(cursor, pygame.mouse.get_pos())

    # Окно перехода на следующий уровень
    if win_status is True:
        if Level == 1 or Level == 2:
            print_text('Нажмите Enter для перехода на следующий уровень', 520, 385)  # Добавление текста на экран
            if keys[pygame.K_RETURN]:  # Проверка на нажатие кнопки Enter
                if Level == 1:
                    boss_group.add(Golem())  # Добавление следующего басса голема
                if Level == 2:
                    boss_group.add(Crystal())  # Добавление следующего босса кристала
                Level += 1

                # Обновление координат
                where_x = sprite.rect.x = 770
                where_y = sprite.rect.y = 660
                win_status = False
                arrow_group.empty()  # Обновление стрел

        # Если игры пройдёна, то выходит экран победы
        elif Level == 3:
            win_screen()

    pygame.display.flip()  # Обновление кадра
    clock.tick(FPS)  # Ограничение частоты кадров
