# Pygame шаблон - скелет для нового проекта Pygame
import pygame
import random
# импортируем рандомно из диапозоне случайных чисел
from random import randrange as rnd

WIDTH=960 # ширина игрового окна
HEIGHT=600 # высота игрового окна
FPS=60 # частота кадров в секунду
#paddle settings (настройки платформы)
paddle_w=330
paddle_h=35
paddle_speed=15




# платформа является встроенным классом rect. Размещать платформу будем посередине
paddle=pygame.Rect(WIDTH//2 - paddle_w//2, HEIGHT - paddle_h - 10, paddle_w, paddle_h)
# ball settings
ball_radius=20
ball_speed=6
ball_rect=int(ball_radius * 2 ** 0.5)
ball=pygame.Rect(rnd(ball_rect, WIDTH - ball_rect), HEIGHT //2, ball_rect, ball_rect)
#ball = pygame.image.load("images/football.png")  хочу заменить мячик

# переменные значений, отвечающие за направление движения и смену движения
dx, dy = 1, -1
# block settings (списком)
block_list = [pygame.Rect(10+120*i, 10+70*j, 100, 50) for  i in range (10) for j in range (4)]
# для эффекта блоки сделаем рандомно
color_list = [(rnd(30,256), rnd(30,256), rnd(30,256)) for  i in range (10) for j in range (4)]

# цвета (r,g,b)
BLACK=(0,0,0)
WHITE=(255,255,255)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)




# создаем окно игры
pygame.init() # это команда, которая запускает pygame
# смена иконки интерфейса
icon = pygame.image.load('images/icon.png')
pygame.display.set_icon(icon)

sound = pygame.mixer.Sound(file='images/click.wav')
pygame.init() # для звука

screen=pygame.display.set_mode((WIDTH, HEIGHT)) # screen - это окно программы
pygame.display.set_caption("My First Game")
clock=pygame.time.Clock() # clock - убедиться, что игра работает с заданной частотой кадров
# background image
img=pygame.image.load('images/nebo.jpg').convert()



# определяем столкновения. пишим в виде отдельной функции
def detect_collision(dx,dy,ball,rect):
    if dx > 0:
        delta_x = ball.right - rect.left
    else:
        delta_x = rect.right - ball.left
    if dy > 0:
        delta_y = ball.bottom - rect.top
    else:
        delta_y = rect.bottom - ball.top


    # 10 пикселей от крайнего блока
    if abs(delta_x - delta_y) < 10:
        dx, dy = -dx, -dy
    elif delta_x > delta_y:
        dy = -dy
    elif delta_y > delta_x:
        dx = -dx
    return dx, dy




# создаем цикл игры
running=True # игровой цикл while, контролируемый переменной running. Если нужно завершить игру, необходимо всего лишь поменять значение на False
while running:
    # ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type==pygame.QUIT:
            exit()
        
    # дердим цикл на правильной скорости
    clock.tick(FPS) # tick - просит определить, сколько времени занимает цикл, а затем сделать паузу, чтобы цикл (целый кадр) длился нужное время. Если хадать FPS 30, это значит, что длина одного кадра - 1/30 (0,03 секунды). Если цикл кода (обновление, рендеринг и пр.) занимает 0,01 секунды, то pygame сделает паузу на 0,02 секунды.
    # обновление
    # рендеринг
    #screen.fill(BLACK)
    screen.blit(img, (0, 0))

    #draw objects for game
    # отображаем блоки в игре
    [pygame.draw.rect(screen, color_list[color], block) for color, block in enumerate (block_list)]
    #отображаем платформу в игре оранжевым цветом
    pygame.draw.rect(screen,pygame.Color('darkorange'),paddle)
    #отображаем шарик в игре
    pygame.draw.circle(screen, pygame.Color('White'), ball.center, ball_radius)
    # делаем движение шарика c учетом его скорости и направления движения
    ball.x +=ball_speed * dx
    ball.y +=ball_speed * dy
    # создаем условие, чтобы шарик не вылетал за пределы левого и правого края
    if ball.centerx < ball_radius or ball.centerx > WIDTH - ball_radius:
        dx= -dx

    # создаем условие, чтобы шарик не вылетал за пределы верхнего края
    if ball.centery < ball_radius:
        dy = -dy
    # определяем столкновение с платформой с помощью метода colliderect, и учесть движение шарика к платформе
    if ball.colliderect(paddle) and dy > 0: # угол падения
        dx, dy = detect_collision(dx,dy,ball,paddle)   # угол отражения

    # коллизия мячика с блоками проверяем и удаляем (и цвет тоже удаляем, и блок с которым столкнулись)
    hit_index = ball.collidelist(block_list)
    if hit_index != -1:
        hit_rect = block_list.pop(hit_index)
        hit_color = color_list.pop(hit_index)
        dx, dy = detect_collision(dx,dy,ball,hit_rect)

        # добавим эффект увеличения квадрата при столкновении, а также увеличим скорость игры
        hit_rect.inflate_ip(ball.width * 3, ball.height * 3)
        pygame.draw.rect(screen,hit_color,hit_rect)
        FPS += 2


    # делаем выход из игры с сообщениями (game over, win!)
    if ball.bottom > HEIGHT:
        print ("GAME OVER!")
        exit()
    elif not len (block_list):
        print("WIN!")
        exit()


    #control key , управление платформой в отдельную переменную
    key=pygame.key.get_pressed()
    #также пишем условие, чтобы платформа не уходила за пределы экрана
    if key[pygame.K_LEFT] and paddle.left > 0:
        paddle.left -= paddle_speed
    if key[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.right += paddle_speed


    # после отрисовки всего, переворачиваем экран
    pygame.display.flip()



pygame.quit()

