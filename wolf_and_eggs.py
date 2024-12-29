import pygame, random, sys
from pygame.locals import *

WIN_WIDTH = 800
WIN_HEIGHT = 600
BlUE_COLOR = (100, 149, 237)
YELLOW_COLOR = (255, 255, 0)
TEXT_COLOR = (0, 0, 0)
BACKGROUND = (255, 255, 255)
FPS = 30

EGG_MIN_SIZE = 30
EGG_MAX_SIZE = 50
EGG_MIN_SPEED = 1
EGG_MAX_SPEED = 5
NEW_EGG_COUNT = 6

PLAYER_SPEED = 5


def close_game():
    """Функция, закрывающая программу"""
    pygame.quit()
    sys.exit()


def waiting_for_press_key():
    """Функция ожидания нажатия клавиши игроком. При нажатии клавиши ESC срабатывает
    функция 'close_game'"""
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                close_game()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    close_game()
                return

# Функция для усовершенствования игры, в случае, если придется добавлять другие объекты кроме яиц.
def is_hit(player, eggs):
    """Функция проверки столкновения игрока с объектами"""
    for egg in eggs:
        if player.colliderect(egg['form']):
            return True
    return False


def is_fallen(eggs):
    """Функция проверки столкновения объектов из списка eggs с нижней границей экрана.
    Возвращает True, если хотя бы один из объект из списка eggs коснулся нижней границы экрана, и False,
    если ниодин объект не коснулся."""
    for egg in eggs:
        if egg['form'].bottom >= WIN_HEIGHT:
            return True
    return False


def draw_text(text, font, surface, x, y):
    """Функция рисования текста (text) определенного шрифта (font) на объект (surface)
    в координатах верхнего левого угла Х и Y"""
    output_text = font.render(text, 1, BlUE_COLOR, YELLOW_COLOR)
    text_form = output_text.get_rect()
    text_form.center = (x, y)
    surface.blit(output_text, text_form)


# Инициализация игры
pygame.init()
game_time = pygame.time.Clock()

# Настройка игрового окна и названия
main_surface = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Волк и яйца")

# Настройка шрифта и звуков
font = pygame.font.SysFont('comicsansms', 23)
pygame.mixer.music.load('main.wav')
pygame.mixer.music.play(-1)
go_sound = pygame.mixer.Sound('game-over.wav')
crush_sound = pygame.mixer.Sound('crush.wav')

# Настройки спрайтов
player_size = 70
player_img = pygame.image.load('wolf.png')
player_img = pygame.transform.scale(player_img, (player_size, player_size))
player_form = player_img.get_rect()
egg_img = pygame.image.load('egg.png')

# Начало игры
main_surface.fill(BACKGROUND)
draw_text("Волк и яйца", font, main_surface, (WIN_WIDTH / 2), (WIN_HEIGHT / 2))
draw_text("Нажмите любую клавишу для начала игры",
          font, main_surface, (WIN_WIDTH / 5) + 250, (WIN_HEIGHT / 3))
pygame.display.update()
waiting_for_press_key()

# Подгружаем лучший результат
with open('top_score.txt', 'r') as file:
    top_score = file.read()

top_score = int(top_score)

# Запускаем основной цикл игры
while True:
    # Изначально список яиц пуст, счет равен нулю
    eggs = []
    score = 0
    player_form.topleft = (WIN_WIDTH / 2, WIN_HEIGHT - 80)
    move_left = move_right = False
    eggs_counter = 0

    # Цикл проверки нажатия клавиш и проверки условий игры
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                close_game()
            if event.type == KEYDOWN:
                if event.key == K_RIGHT or event.key == K_d:
                    move_right = True
                if event.key == K_LEFT or event.key == K_a:
                    move_left = True

            if event.type == KEYUP:
                if event.key == K_RIGHT or event.key == K_d:
                    move_right = False
                if event.key == K_LEFT or event.key == K_a:
                    move_left = False

            if event.type == MOUSEMOTION:
                player_form.centerx = event.pos[0]

        eggs_counter += 1
        # Если счетчик циклов программы дошел до необходимого числа, чтобы создать новое яйцо
        if eggs_counter == NEW_EGG_COUNT:
            eggs_counter = 0
            egg_size = random.randint(EGG_MIN_SIZE, EGG_MAX_SIZE)
            egg_speed = random.randint(EGG_MIN_SPEED, EGG_MAX_SPEED)
            # Создаем словарь для обхекта яйцо, в котором три ключа: форма, скорость и картинка.
            # Добавляем объект в список всех яиц.
            new_egg = {'form':
                           pygame.Rect(random.randint(0, WIN_WIDTH - egg_size),
                                       0 - egg_size,
                                       egg_size,
                                       egg_size
                                       ),
                       'speed': egg_speed,
                       'surface': pygame.transform.scale(egg_img,
                                                         (egg_size, egg_size))
                       }
            eggs.append(new_egg)

        # Проверка: если клавиша влево/вправо нажата и границы экрана позволяют двигаться,
        # то переместить спрайт волка
        if move_left and player_form.left > 0:
            player_form.move_ip(-1 * PLAYER_SPEED, 0)

        if move_right and player_form.right < WIN_WIDTH:
            player_form.move_ip(PLAYER_SPEED, 0)

        # Выполняем движение яиц.
        for egg in eggs:
            egg['form'].move_ip(0, egg['speed'])

        # Проверка: коснулся ли волк яйцо
        for egg in eggs[:]:
            if player_form.colliderect(egg['form']):
                score += 1
                eggs.remove(egg)

        # Отображение игры.
        main_surface.fill(BACKGROUND)
        draw_text(f'Cчет: {score}', font, main_surface, 70, 20)
        draw_text(f'Рекорд: {top_score}', font, main_surface, 70, 50)
        main_surface.blit(player_img, player_form)

        for egg in eggs:
            main_surface.blit(egg['surface'], egg['form'])

        pygame.display.update()

        # Проверка, если яйцо коснулось нижней границы экрана
        if is_fallen(eggs):
            crush_sound.play()
            if score > top_score:
                top_score = score
                with open('top_score.txt', 'w') as file:
                    file.write(f'{top_score}')
            break

        game_time.tick(FPS)
    pygame.mixer.music.stop()
    go_sound.play(-1)
    draw_text("Game Over", font, main_surface, (WIN_WIDTH / 2), (WIN_HEIGHT / 2))
    pygame.display.update()
    waiting_for_press_key()
    go_sound.stop()
    pygame.mixer.music.play(-1)
