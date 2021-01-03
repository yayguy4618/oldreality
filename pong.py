import pygame
import random

# Инициализация pygame
pygame.init()
clock = pygame.time.Clock()

# Глобальные переменные
screen_width = 1600
screen_height = 1400
ball_size = 30
play_height = 1198
play_width = 1500
top_left_x = (screen_width - play_width) // 2
top_left_y = screen_height - play_height - 2

# Рисование основных элементов окна
ball = pygame.Rect(play_width / 2 - ball_size / 2, play_height / 2 - ball_size / 2,
                   ball_size, ball_size)
opponent = pygame.Rect(play_width + 20, play_height / 2 + 70, 10, 140)
player = pygame.Rect(70, play_height / 2 + 70, 10, 140)
border = pygame.Rect(top_left_x, top_left_y, play_width, play_height)

# Переменные цвета
bg_color = (0, 0, 0)
green = (0, 255, 0)

# Переменные скорости
v_x = 7
v_y = 7
v_player = 0
v_opponent = 7

# Время
time = True


# Счет
player_score = 0
opponent_score = 0

# Звук
bounce = pygame.mixer.Sound("data/pong.ogg")
win = pygame.mixer.Sound("data/score.ogg")


def ai():
    if ball.x > screen_width / 2:
        if opponent.top < ball.y:
            opponent.top += v_opponent
        elif opponent.bottom > ball.y:
            opponent.bottom -= v_opponent
        if opponent.top <= top_left_y:
            opponent.top = top_left_y
        elif opponent.bottom >= screen_height:
            opponent.bottom = screen_height


def restart():
    global v_x, v_y, time

    ball.center = (play_width / 2 + top_left_x, play_height / 2 + top_left_y)
    current_time = pygame.time.get_ticks()

    if current_time - time < 700:
        draw_text_middle("3", 100, (0, 255, 0), window, delta_x=100, delta_y=150)
        v_x, v_y = 0, 0
    elif current_time - time < 1400:
        draw_text_middle("2", 100, (0, 255, 0), window, delta_x=100, delta_y=150)
        v_x, v_y = 0, 0
    elif current_time - time < 2100:
        draw_text_middle("1", 100, (0, 255, 0), window, delta_x=100, delta_y=150)
        v_x, v_y = 0, 0
    else:
        v_y = 7 * random.choice((-1, 1))
        v_x = 7 * random.choice((-1, 1))
        time = None


def draw_ball():
    global v_x, v_y, time, opponent_score, player_score
    ball.x += v_x
    ball.y += v_y

    if ball.top <= top_left_y or ball.bottom >= play_height + top_left_y:
        v_y *= -1
        pygame.mixer.Sound.play(bounce)
    if ball.left <= top_left_x:
        opponent_score += 1
        time = pygame.time.get_ticks()
        pygame.mixer.Sound.play(win)
    elif ball.right > top_left_x + play_width:
        player_score += 1
        time = pygame.time.get_ticks()
        pygame.mixer.Sound.play(win)
    if ball.colliderect(opponent) and v_x > 0:
        pygame.mixer.Sound.play(bounce)
        v_x *= -1
    if ball.colliderect(player) and v_x < 0:
        pygame.mixer.Sound.play(bounce)
        v_x *= -1


def draw_player():
    player.y += v_player
    if player.top <= top_left_y:
        player.top = top_left_y
    if player.bottom >= screen_height:
        player.bottom = screen_height


def draw_text_middle(text, size, color, surface, delta_x=0, delta_y=0):
    font = pygame.font.Font('data/font.ttf', size)
    label = font.render(text, True, color)

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2) + delta_x,
                         top_left_y + play_height / 2 - label.get_height() * 2 + delta_y))


def main():
    global v_player
    running = True
    paused = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    v_player += 7
                elif event.key == pygame.K_UP:
                    v_player -= 7
                if event.key == pygame.K_SPACE:
                    paused = not paused

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    v_player -= 7
                elif event.key == pygame.K_UP:
                    v_player += 7
        if not paused:
            draw_ball()
            draw_player()
            ai()

            window.fill(bg_color)
            pygame.draw.rect(window, green, player)
            pygame.draw.rect(window, green, opponent)
            pygame.draw.aaline(window, green, (screen_width / 2, top_left_y), (screen_width / 2, screen_height))
            pygame.draw.rect(window, green, ball)
            pygame.draw.rect(window, green, border, 5)
        else:
            window.fill((0, 0, 0))
            draw_text_middle('Paused', 60, (0, 255, 0), window)
            pygame.display.update()
            paused = check_pause(paused)
            continue

        if time:
            restart()

        draw_text_middle("Pong", 100, (0, 255, 0), window, delta_y=-550)
        draw_text_middle(f"{player_score}:{opponent_score}", 50, (0, 255, 0), window, delta_y=-550)
        pygame.display.flip()
        clock.tick(60)


def check_pause(paused):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
    return paused


def main_menu():
    run = True
    while run:
        window.fill((0, 0, 0))

        draw_text_middle('Press any key to begin.', 60, (0, 255, 0), window)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                main()
    pygame.quit()


# Объявление окна
window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong')

main_menu() # Запуск игры
