import copy as copy
import random
import sys
import time


#import numpy as nps
import pygame as pg

fps = 60
real_tile_size = 16
scale = 4
tile_size = real_tile_size * scale
grid_size_x = int(64/scale)
grid_size_y = int(64/scale)
screen_size_x = grid_size_x * tile_size
screen_size_y = grid_size_y * tile_size
screen = pg.display.set_mode((screen_size_x, screen_size_y))
pg.display.set_caption("snake")
background = pg.image.load('../Snake-AI/sprites/white.png').convert()
background = pg.transform.scale(background, (tile_size, tile_size))
number_of_fruits = 1
pg.init()


def snek():
    keys = []
    running = True
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

    class Fruit:
        def __init__(self):
            self.location = [-1, -1]
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
            self.head_sprite = pg.image.load('../Snake-AI/sprites/snek.png').convert()
            self.head_sprite = pg.transform.scale(self.head_sprite, (tile_size, tile_size))
            self.body_sprite = pg.image.load('../Snake-AI/sprites/body.png').convert()
            self.body_sprite = pg.transform.scale(self.body_sprite, (tile_size, tile_size))
            self.rotation = 0
            self.direction = 0
            self.is_alive = True

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

        def collision_body(self):
            if len(self.body) > 0:
                for body_part in range(1, len(self.body)):
                    if self.body[body_part] == [self.pos_x, self.pos_y]:
                        self.is_alive = False

        def collision_fruit(self, Fruit):
            if [self.pos_x, self.pos_y] == Fruit.location:
                self.body.append([-1, -1])
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
                self.head_sprite = pg.transform.rotate(self.head_sprite, self.rotation - 270)
                self.rotation = 270
                return
            if keys[0] == 'd' and self.direction != 1:
                self.direction = 2
                self.head_sprite = pg.transform.rotate(self.head_sprite, self.rotation - 90)
                self.rotation = 90
                return
            if keys[0] == 'w' and self.direction != 4:
                self.direction = 3
                self.head_sprite = pg.transform.rotate(self.head_sprite, self.rotation)
                self.rotation = 0
                return
            if keys[0] == 's' and self.direction != 3:
                self.direction = 4
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
    for x in range(0, number_of_fruits):
        fruits['fruit ' + str(x)] = Fruit()
        fruits['fruit ' + str(x)].generate(snake.body)
    tick = int(fps/10)
    while running:
        if tick == int(fps/10):
            screen.fill((255, 255, 255))
            running = get_input(running)
            snake.update(keys)
            if len(keys) >= 1:
                keys.pop(0)
            snake.draw()
            for x in range(0, number_of_fruits):
                fruits['fruit ' + str(x)].location = snake.collision_fruit(fruits['fruit ' + str(x)])
                fruits['fruit ' + str(x)].draw()
            tick = 0
            draw_score()
            pg.display.update()
        tick = tick + 1
        clock.tick(fps)
        if not snake.is_alive:
            running = False


snek()
