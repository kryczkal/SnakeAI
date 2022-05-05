import copy as copy
import random
import time

import numpy as np
import pygame as pg


def snek():
    real_tile_size = 16
    scale = 4
    tile_size = real_tile_size * scale
    x_size = 16
    y_size = 16
    screen_size = [y_size * tile_size, x_size * tile_size]
    ascii_graphics = ["."]
    board = np.full((y_size, x_size), ascii_graphics[0])
    snake_pos = [random.randrange(0, x_size - 1), random.randrange(0, y_size - 1)]
    board[snake_pos[1], snake_pos[0]] = "s"
    body = [[-1, -1]]
    snek_rotation = 0
    fruit = [1, 1]
    direction = 0
    speed = 150
    speed_mode = 0

    # 1 = x, 0 = y
    def screen_set_hehe(x, y, z):
        for c in range(0, z):
            screen.set_at((x + c, y), "BLACK")

    def game_over():
        pg.mixer.music.fadeout(500)
        pg.mixer.fadeout(500)
        def animation():
            falling = pg.mixer.Sound('../Snake-AI/sounds/fall.mp3')
            wasted = pg.mixer.Sound('../Snake-AI/sounds/wasted.mp3')
            z = 25
            falling.play()
            time.sleep(0.5)
            for x in range(0, int(screen_size[1]), z):
                for y in range(0, screen_size[0]):
                    screen_set_hehe(x, y, z)
                    if y % 20 == 0:
                        pg.display.update()
                pg.display.update()
            pg.mixer.fadeout(100)
            wasted.play()
            time.sleep(1)
            for x in range(0, 500):
                font = pg.font.SysFont('arial', int(tile_size * x_size / (len('GAME OVER') - 1)))
                fotn = font.render('GAME OVER', True, 'WHITE')
                q, w = pg.font.Font.size(font, 'GAME OVER')  # dimensions of text object
                screen.fill((0, 0, 0))
                screen.blit(fotn, (
                    int(screen_size[1] / 10) + random.randrange(-10, 10),
                    int(screen_size[0] / 2) + random.randrange(-10, 10)))
                pg.display.update()
        #animation()
        return False

    def collision_body(body, snake_pos):
        if len(body) > 0:
            for x in range(1, len(body)):
                # print([snake_pos, body[x]])
                if body[x] == snake_pos:
                    print("gae over")
                    return 1

    def collision_fruit(fruit, snake_pos):
        if snake_pos == fruit:
            body.append([-1, -1])
            fruit_sound.play()
            fruit = generate_fruit(fruit)
        return fruit

    def generate_fruit(fruit):
        fruit = [random.randrange(0, x_size), random.randrange(0, y_size)]
        for x in body:
            if x == fruit:
                fruit = generate_fruit(fruit)
        return fruit

    def correction():
        if snake_pos[1] > y_size - 1:
            snake_pos[1] = 0
        if snake_pos[1] < 0:
            snake_pos[1] = y_size - 1

        if snake_pos[0] > x_size - 1:
            snake_pos[0] = 0
        if snake_pos[0] < 0:
            snake_pos[0] = x_size - 1

    def direction_module(direction, snake_pos, body):
        if direction == 1:
            snake_pos[0] = snake_pos[0] - 1
        if direction == 2:
            snake_pos[0] = snake_pos[0] + 1
        if direction == 3:
            snake_pos[1] = snake_pos[1] - 1
        if direction == 4:
            snake_pos[1] = snake_pos[1] + 1
        correction()
        body_update(body, snake_pos)

    def movement(snek, snek_rotation, body, snake_pos, direction):
        if keys[0] == 'a' and direction != 2:
            direction = 1
            snek = pg.transform.rotate(snek, snek_rotation - 270)
            snek_rotation = 270
            return [snek, snek_rotation, direction]
        if keys[0] == 'd' and direction != 1:
            direction = 2
            snek = pg.transform.rotate(snek, snek_rotation - 90)
            snek_rotation = 90
            return [snek, snek_rotation, direction]
        if keys[0] == 'w' and direction != 4:
            direction = 3
            snek = pg.transform.rotate(snek, snek_rotation)
            snek_rotation = 0
            return [snek, snek_rotation, direction]
        if keys[0] == 's' and direction != 3:
            direction = 4
            snek = pg.transform.rotate(snek, snek_rotation - 180)
            snek_rotation = 180
            return [snek, snek_rotation, direction]
        if len(keys) > 1:
            keys.pop(0)
            movement(snek, snek_rotation, body, snake_pos, direction)
        return [snek, snek_rotation, direction]

    def body_update(body, snake_pos):
        # print(len(body))
        if len(body) > 0:
            for x in range(len(body) - 1, -1, -1):
                # print(x)
                body[x] = body[x - 1]
        # print(body)
        body[0] = copy.copy(snake_pos)

    pg.init()
    screen = pg.display.set_mode((screen_size[1], screen_size[0]))
    pg.display.set_caption("snek")
    background = pg.image.load('../Snake-AI/sprites/sand.png').convert()
    background = pg.transform.scale(background, (tile_size, tile_size))
    snek = pg.image.load('../Snake-AI/sprites/snek.png').convert()
    snek = pg.transform.scale(snek, (tile_size, tile_size))
    body_sprite = pg.image.load('../Snake-AI/sprites/body.png').convert()
    body_sprite = pg.transform.scale(body_sprite, (tile_size, tile_size))
    fruit = generate_fruit(fruit)
    fruit_sprite = pg.image.load('../Snake-AI/sprites/fruit.png').convert()
    fruit_sprite = pg.transform.scale(fruit_sprite, (tile_size, tile_size))
    #pg.mixer.music.load('../Snake-AI/sounds/music.mp3')
    #pg.mixer.music.set_volume(0.1)
    #pg.mixer.music.play()

    fruit_sound = pg.mixer.Sound('../Snake-AI/sounds/fruit.mp3')
    fruit_sound.set_volume(0.3)
    keys = []
    running = True
    while running:
        startTime = time.time()
        screen.fill((0, 0, 0))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_s:
                    keys.append("s")
                if event.key == pg.K_w:
                    keys.append("w")
                if event.key == pg.K_d:
                    keys.append('d')
                if event.key == pg.K_a:
                    keys.append('a')
        if len(keys) >= 1:
            #print(len(keys))
            a = movement(snek, snek_rotation, body, snake_pos, direction)
            snek = a[0]
            snek_rotation = a[1]
            direction = a[2]
            keys.pop(0)
        direction_module(direction, snake_pos, body)
        fruit = collision_fruit(fruit, snake_pos)
        # print(board)
        board = np.full((screen_size[1], screen_size[0]), ascii_graphics[0])
        board[snake_pos[1], snake_pos[0]] = "s"
        board[fruit[1], fruit[0]] = "f"
        if len(body) > 0:
            for x in range(0, len(body) - 1):
                board[body[x + 1][1], body[x + 1][0]] = "b"
        for x in range(0, x_size):
            for y in range(0, y_size):
                if board[y][x] == ".":
                    screen.blit(background, (x * tile_size, y * tile_size))
                if board[y][x] == "s":
                    screen.blit(snek, (x * tile_size, y * tile_size))
                if board[y][x] == "b":
                    screen.blit(body_sprite, (x * tile_size, y * tile_size))
                if board[y][x] == "f":
                    screen.blit(fruit_sprite, (x * tile_size, y * tile_size))
        font = pg.font.SysFont(None, 16 * scale)
        img = font.render(str(len(body)), True, 'BLACK')
        screen.blit(img, (20, 20))
        pg.display.update()
        if collision_body(body, snake_pos) == 1:
            running = game_over()
        # if speed < 100:
        #    speed_mode = 1
        #    speed = 102
        # if speed_mode == 0:
        #    speed = speed - 1.5
        # else:
        #    speed = speed - 1.5
        pg.time.delay(int(speed - (time.time() - startTime)))


snek()