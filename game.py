import copy as copy
import random
import sys
import time

import numpy as np
import pygame as pg

graphic_on = True
fps_on = False


def Framerate_on():
    global fps_on
    fps_on = True


fps = 15
real_tile_size = 16
scale = 4
tile_size = real_tile_size * scale
grid_size_x = int(64 / scale)
grid_size_y = int(64 / scale)
screen_size_x = grid_size_x * tile_size
screen_size_y = grid_size_y * tile_size
score = 0
if graphic_on:
    screen = pg.display.set_mode((screen_size_x, screen_size_y))
    pg.display.set_caption("snake")
    background = pg.image.load('../Snake-AI/sprites/white.png').convert()
    background = pg.transform.scale(background, (tile_size, tile_size))
    pg.init()
number_of_fruits = 1

keys = []
clock = pg.time.Clock()


def get_input(run):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_s:
                keys.append('s')
            if event.key == pg.K_w:
                keys.append('w')
            if event.key == pg.K_d:
                keys.append('d')
            if event.key == pg.K_a:
                keys.append('a')
    return run


def draw_score():
    font = pg.font.SysFont(None, int(tile_size))
    img = font.render(str(len(snake.body)), True, 'BLACK')
    screen.blit(img, (20, 20))


def state_of_game():
    global snake
    d_up, d_down, d_left, d_right = snake.danger_detection()
    m_up, m_down, m_left, m_right = snake.direction_detection()
    f_up, f_down, f_left, f_right = snake.fruits_detection()
    # print(snake.direction_detection())
    # print(m_up,m_down,m_left,m_right)
    if m_up == 1:
        state = [d_up, d_right, d_left,
                 m_up, m_down, m_left, m_right,
                 f_up, f_down, f_left, f_right]
    if m_down == 1:
        state = [d_down, d_left, d_right,
                 m_up, m_down, m_left, m_right,
                 f_up, f_down, f_left, f_right]
    if m_left == 1:
        state = [d_left, d_up, d_down,
                 m_up, m_down, m_left, m_right,
                 f_up, f_down, f_left, f_right]
    if m_right == 1:
        state = [d_right, d_down, d_up,
                 m_up, m_down, m_left, m_right,
                 f_up, f_down, f_left, f_right]
    return state


class Fruit:
    def __init__(self):
        self.location = [-1, -1]
        if graphic_on:
            self.sprite = pg.image.load('../Snake-AI/sprites/fruit.png')
            self.sprite = pg.transform.scale(self.sprite, (tile_size, tile_size))
            self.sound = pg.mixer.Sound('../Snake-AI/sounds/fruit.mp3')
            self.sound.set_volume(0.3)

    def generate(self, snake_body):
        self.location = [random.randrange(0, grid_size_x), random.randrange(0, grid_size_y)]
        for body_part in snake_body:
            if body_part == self.location:
                self.location = self.generate(snake_body)
        return self.location

    def draw(self):
        screen.blit(self.sprite, (self.location[0] * tile_size, self.location[1] * tile_size))


class Snake:
    def __init__(self):
        self.pos_x = random.randrange(0, grid_size_x - 1)
        self.pos_y = random.randrange(0, grid_size_y - 1)
        self.body = [[-1, -1]]
        if graphic_on:
            self.head_sprite = pg.image.load('../Snake-AI/sprites/snek.png').convert()
            self.head_sprite = pg.transform.scale(self.head_sprite, (tile_size, tile_size))
            self.body_sprite = pg.image.load('../Snake-AI/sprites/body.png').convert()
            self.body_sprite = pg.transform.scale(self.body_sprite, (tile_size, tile_size))
        self.rotation = 0
        self.direction = random.randint(1, 4)
        self.is_alive = True

    def direction_detection(self):
        up = 0
        down = 0
        left = 0
        right = 0
        if self.direction == 1:
            left = 1
        if self.direction == 2:
            right = 1
        if self.direction == 3:
            up = 1
        if self.direction == 4:
            down = 1
        return up, down, left, right

    def movement(self):
        if self.direction == 1:
            self.pos_x = self.pos_x - 1
        if self.direction == 2:
            self.pos_x = self.pos_x + 1
        if self.direction == 3:
            self.pos_y = self.pos_y - 1
        if self.direction == 4:
            self.pos_y = self.pos_y + 1

    def pos_correction(self):
        if self.pos_y > grid_size_y - 1:
            self.pos_y = 0
        if self.pos_y < 0:
            self.pos_y = grid_size_y - 1

        if self.pos_x > grid_size_x - 1:
            self.pos_x = 0
        if self.pos_x < 0:
            self.pos_x = grid_size_x - 1

    def danger_detection(self):
        global grid_size_y
        global grid_size_x
        up = 0
        down = 0
        left = 0
        right = 0
        point_right = ((self.pos_x - 1)%grid_size_x, self.pos_y)
        point_left = ((self.pos_x - 1)%grid_size_x, self.pos_y)
        point_up = (self.pos_x, (self.pos_y - 1)%grid_size_y)
        point_down = (self.pos_y, (self.pos_y + 1)%grid_size_y)
        for body_part in range(1, len(self.body)):
            if body_part == point_right:
                right = 1
            if body_part == point_left:
                left = 1
            if body_part == point_down:
                down = 1
            if body_part == point_up:
                up = 1

        return up, down, left, right

    def fruits_detection(self):
        global fruits
        fruit = fruits['fruit ' + str(0)]
        fruit_x = fruit.location[0]
        fruit_y = fruit.location[1]
        up = 0
        down = 0
        left = 0
        right = 0
        if fruit_x > self.pos_x:
            right = 1
        elif fruit_x < self.pos_x:
            left = 1
        if fruit_y > self.pos_y:
            up = 1
        elif fruit_y < self.pos_y:
            down = 1
        return up, down, left, right

    def collision_body(self):
        if len(self.body) > 0:
            for body_part in range(1, len(self.body)):
                if self.body[body_part] == [self.pos_x, self.pos_y]:
                    self.is_alive = False

    def collision_fruit(self, Fruit):
        global reward
        if [self.pos_x, self.pos_y] == Fruit.location:
            self.body.append([-1, -1])
            reward += 10
            if graphic_on:
                Fruit.sound.play()
            Fruit.location = Fruit.generate(self.body)
        return Fruit.location

    def tail_update(self):
        if len(self.body) > 0:
            for body_part in range(len(self.body) - 1, -1, -1):
                self.body[body_part] = self.body[body_part - 1]
        self.body[0] = copy.copy([self.pos_x, self.pos_y])

    def handle_input(self, keys):
        if keys[0] == 'a' and self.direction != 2:
            self.direction = 1
            if graphic_on:
                self.head_sprite = pg.transform.rotate(self.head_sprite, self.rotation - 270)
            self.rotation = 270
            return
        if keys[0] == 'd' and self.direction != 1:
            self.direction = 2
            if graphic_on:
                self.head_sprite = pg.transform.rotate(self.head_sprite, self.rotation - 90)
            self.rotation = 90
            return
        if keys[0] == 'w' and self.direction != 4:
            self.direction = 3
            if graphic_on:
                self.head_sprite = pg.transform.rotate(self.head_sprite, self.rotation)
            self.rotation = 0
            return
        if keys[0] == 's' and self.direction != 3:
            self.direction = 4
            if graphic_on:
                self.head_sprite = pg.transform.rotate(self.head_sprite, self.rotation - 180)
            self.rotation = 180
            return

    def draw(self):
        if len(self.body) > 0:
            for body_part in range(1, len(self.body)):
                screen.blit(self.body_sprite,
                            (self.body[body_part][0] * tile_size, self.body[body_part][1] * tile_size))
        screen.blit(self.head_sprite, (self.pos_x * tile_size, self.pos_y * tile_size))

    def update(self, keys):
        if len(keys) >= 1:
            self.handle_input(keys)
        self.movement()
        self.pos_correction()
        self.tail_update()
        self.collision_body()


snake = Snake()
fruits = {}
tick = int(fps / 10)


def restart():
    global snake
    global fruits
    global running
    global keys
    keys = []
    if graphic_on:
        pg.init()
    running = False
    snake = Snake()
    fruits = {}
    for x in range(0, number_of_fruits):
        fruits['fruit ' + str(x)] = Fruit()
        fruits['fruit ' + str(x)].generate(snake.body)


running = True


def Score():
    global score
    return score


def Reward():
    global reward
    return reward


def key_pressed(move):
    global snake
    # print(move)
    if snake.direction == 1:
        if move[0] == 1:
            return 'a'
        if move[1] == 1:
            return 'w'
        if move[2] == 1:
            return 's'
    if snake.direction == 2:
        if move[0] == 1:
            return 'd'
        if move[1] == 1:
            return 's'
        if move[2] == 1:
            return 'w'
    if snake.direction == 3:
        if move[0] == 1:
            return 's'
        if move[1] == 1:
            return 'a'
        if move[2] == 1:
            return 'd'
    if snake.direction == 4:
        if move[0] == 1:
            return 'w'
        if move[1] == 1:
            return 'd'
        if move[2] == 1:
            return 'a'


reward = 0


def next_frame(final_move):
    global tick
    global snake
    global running
    global score
    global keys
    # print(keys)
    global reward
    reward = 0
    if not running:
        if graphic_on:
            screen.fill((255, 255, 255))
        # running = get_input(running)
        snake.update(key_pressed(final_move))
        # print(keys)
        # if len(keys) >= 1:
        #    keys.pop(0)
        if graphic_on:
            snake.draw()

        for x in range(0, number_of_fruits):
            fruits['fruit ' + str(x)].location = snake.collision_fruit(fruits['fruit ' + str(x)])
            if graphic_on:
                fruits['fruit ' + str(x)].draw()
        tick = 0
        score = len(snake.body)
        if graphic_on:
            draw_score()
            pg.display.update()
        if fps_on:
            clock.tick(fps)
        if not snake.is_alive:
            running = True
            reward -= 10
    return running
